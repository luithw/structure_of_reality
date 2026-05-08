#!/usr/bin/env python3
"""Simple comment server for Jekyll blog. Stores comments in SQLite."""

import json
import sqlite3
import time
import re
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "comments.db")
PORT = int(os.environ.get("COMMENTS_PORT", 8080))

# ── Database setup ──

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_slug TEXT NOT NULL,
            author_name TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at INTEGER NOT NULL
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_comments_post
        ON comments(post_slug, created_at DESC)
    """)
    conn.commit()
    conn.close()

# ── HTTP Handler ──

class CommentHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # suppress noisy stdout logs

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length).decode("utf-8")

    def do_OPTIONS(self):
        self._send_json({})

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/comments":
            params = parse_qs(parsed.query)
            post_slug = params.get("post_slug", [None])[0]
            if not post_slug:
                self._send_json({"error": "post_slug is required"}, 400)
                return
            conn = get_db()
            rows = conn.execute(
                "SELECT id, post_slug, author_name, body, created_at "
                "FROM comments WHERE post_slug = ? ORDER BY created_at ASC",
                (post_slug,)
            ).fetchall()
            conn.close()
            comments = [dict(r) for r in rows]
            self._send_json({"comments": comments})
        else:
            self._send_json({"error": "not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/comments":
            try:
                body = json.loads(self._read_body())
            except json.JSONDecodeError:
                self._send_json({"error": "invalid JSON"}, 400)
                return

            post_slug = (body.get("post_slug") or "").strip()
            author_name = (body.get("author_name") or "").strip()
            comment_body = (body.get("body") or "").strip()

            errors = []
            if not post_slug:
                errors.append("post_slug is required")
            if not author_name:
                errors.append("author_name is required")
            elif len(author_name) > 80:
                errors.append("author_name must be 80 characters or fewer")
            if not comment_body:
                errors.append("body is required")
            elif len(comment_body) > 2000:
                errors.append("body must be 2000 characters or fewer")

            if errors:
                self._send_json({"error": "; ".join(errors)}, 400)
                return

            conn = get_db()
            cur = conn.execute(
                "INSERT INTO comments (post_slug, author_name, body, created_at) VALUES (?, ?, ?, ?)",
                (post_slug, author_name, comment_body, int(time.time()))
            )
            comment_id = cur.lastrowid
            conn.commit()
            conn.close()

            self._send_json({
                "id": comment_id,
                "post_slug": post_slug,
                "author_name": author_name,
                "body": comment_body,
                "created_at": int(time.time())
            }, 201)
        else:
            self._send_json({"error": "not found"}, 404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        match = re.match(r"^/api/comments/(\d+)$", parsed.path)
        if match:
            comment_id = int(match.group(1))
            conn = get_db()
            cur = conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
            conn.commit()
            if cur.rowcount == 0:
                conn.close()
                self._send_json({"error": "comment not found"}, 404)
                return
            conn.close()
            self._send_json({"deleted": True})
        else:
            self._send_json({"error": "not found"}, 404)


if __name__ == "__main__":
    init_db()
    server = HTTPServer(("0.0.0.0", PORT), CommentHandler)
    print(f"Comment server running on http://0.0.0.0:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()
