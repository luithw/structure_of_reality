#!/usr/bin/env python3
"""Simple comment and newsletter server for Jekyll blog. Stores data in SQLite."""

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
    
    # Comments table
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
    
    # Newsletter subscribers table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS newsletter_subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            subscribed_at INTEGER NOT NULL,
            confirmed INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_newsletter_email
        ON newsletter_subscribers(email)
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

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # ── Comments API ──

    def do_GET(self):
        parsed = urlparse(self.path)
        
        # GET /api/comments?post_slug=...
        if parsed.path == "/api/comments":
            qs = parse_qs(parsed.query)
            post_slug = qs.get("post_slug", [None])[0]
            
            if not post_slug:
                self._send_json({"error": "post_slug required"}, 400)
                return
            
            conn = get_db()
            comments = conn.execute(
                "SELECT id, post_slug, author_name, body, created_at FROM comments WHERE post_slug = ? ORDER BY created_at DESC",
                (post_slug,)
            ).fetchall()
            conn.close()
            
            self._send_json({
                "post_slug": post_slug,
                "comments": [dict(c) for c in comments]
            })
        else:
            self._send_json({"error": "not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_json({"error": "invalid json"}, 400)
            return
        
        # POST /api/comments
        if parsed.path == "/api/comments":
            post_slug = data.get("post_slug", "").strip()
            author_name = data.get("author_name", "").strip()
            comment_body = data.get("body", "").strip()
            
            if not post_slug or not author_name or not comment_body:
                self._send_json({"error": "post_slug, author_name, and body required"}, 400)
                return
            
            if len(comment_body) > 5000:
                self._send_json({"error": "comment too long (max 5000 chars)"}, 400)
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
        
        # POST /api/newsletter/subscribe
        elif parsed.path == "/api/newsletter/subscribe":
            email = data.get("email", "").strip().lower()
            
            if not email:
                self._send_json({"error": "email required"}, 400)
                return
            
            # Basic email validation
            if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
                self._send_json({"error": "invalid email"}, 400)
                return
            
            conn = get_db()
            try:
                cur = conn.execute(
                    "INSERT INTO newsletter_subscribers (email, subscribed_at, confirmed) VALUES (?, ?, ?)",
                    (email, int(time.time()), 1)
                )
                subscriber_id = cur.lastrowid
                conn.commit()
                conn.close()
                
                self._send_json({
                    "id": subscriber_id,
                    "email": email,
                    "subscribed_at": int(time.time()),
                    "message": "Successfully subscribed to newsletter!"
                }, 201)
            except sqlite3.IntegrityError:
                conn.close()
                self._send_json({"error": "email already subscribed"}, 409)
            except Exception as e:
                conn.close()
                self._send_json({"error": str(e)}, 500)
        
        else:
            self._send_json({"error": "not found"}, 404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        
        # DELETE /api/comments/{id}
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
    print(f"Comment and newsletter server running on http://0.0.0.0:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()
