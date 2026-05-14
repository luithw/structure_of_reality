#!/usr/bin/env python3
"""scripts/send_custom_newsletter_notification.py

Send newsletter emails using your own backend subscriber store.

This script:
- Reads subscribers from the SQLite DB table `newsletter_subscribers`.
- Builds an email from a Jekyll post file.
- Sends via SMTP.

Why SMTP?
- Because if we are no longer using Buttondown, we still need an email delivery provider.

Dry run:
- Set DRY_RUN=1 to verify what would be sent (no emails sent).

Usage:
  # Send the latest post (default behavior — no arguments needed):
  DRY_RUN=1 python3 scripts/send_custom_newsletter_notification.py

  # Or specify a post manually:
  DRY_RUN=1 python3 scripts/send_custom_newsletter_notification.py \
    _posts/2026-04-18-three-ways-to-store-a-note.md \
    "https://example.com/2026/04/18/three-ways-to-store-a-note/"

Environment variables:
  COMMENTS_DB_PATH   Path to comments.db (default: repo_root/comments.db)

  SMTP_HOST          SMTP server host (required unless DRY_RUN=1)
  SMTP_PORT          SMTP server port (default: 587)
  SMTP_USERNAME      SMTP username (optional)
  SMTP_PASSWORD      SMTP password (optional)
  SMTP_USE_TLS       1/true to start TLS (default: 1)

  EMAIL_FROM         From email address (optional; falls back to _config.yml: email: or 'lui.thw@gmail.com')
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import secrets
import smtplib
import sqlite3
from email.message import EmailMessage
from urllib.parse import urlparse

def _load_dotenv():
    """Load .env file from the repo root into os.environ (simple, no dependencies)."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(repo_root, ".env")
    if not os.path.isfile(env_path):
        return
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            if key and key not in os.environ:
                os.environ[key] = value


EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

TAYIS_BASE_URL = "https://tayis.io/u/tim-lui/p/structure-of-reality/"


def to_tayis_post_url(post_url: str) -> str:
    """Re-root a post URL to the Tayis base URL.

    If the input is already on Tayis, the Tayis base path is removed to avoid duplication.
    """
    base_parsed = urlparse(TAYIS_BASE_URL)
    base_path = (base_parsed.path or "").rstrip("/")
    base_root = TAYIS_BASE_URL.rstrip("/")

    parsed = urlparse(post_url)
    path = parsed.path if (parsed.scheme and parsed.netloc) else post_url

    path_stripped = path
    if base_path and path_stripped.startswith(base_path + "/"):
        path_stripped = path_stripped[len(base_path):]
    if not path_stripped.startswith("/"):
        path_stripped = "/" + path_stripped

    # If the path doesn't end with .html, append it
    if not path_stripped.endswith(".html"):
        # Remove trailing slash first, then add .html
        if path_stripped.endswith("/"):
            path_stripped = path_stripped[:-1]
        # Only add .html if it looks like a post path (not an asset)
        if "." not in path_stripped.rsplit("/", 1)[-1]:
            path_stripped = path_stripped + ".html"

    return base_root + path_stripped


POST_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.md$")


def find_latest_post() -> str:
    """Scan _posts/ and return the path to the newest post file (by filename date)."""
    posts_dir = os.path.join(repo_root(), "_posts")
    candidates = glob.glob(os.path.join(posts_dir, "*.md"))
    dated: list[tuple[str, str]] = []
    for p in candidates:
        m = POST_RE.match(os.path.basename(p))
        if m:
            dated.append((f"{m.group(1)}{m.group(2)}{m.group(3)}", p))
    if not dated:
        raise SystemExit("No dated _posts/*.md files found")
    dated.sort(key=lambda x: x[0], reverse=True)
    return dated[0][1]


def post_to_tayis_url(post_path: str) -> str:
    """Convert a _posts filename to the full Tayis URL."""
    basename = os.path.basename(post_path)
    m = POST_RE.match(basename)
    if not m:
        # fallback: just re-root the path
        return to_tayis_post_url(post_path)
    path_part = f"/{m.group(1)}/{m.group(2)}/{m.group(3)}/{m.group(4)}.html"
    return TAYIS_BASE_URL.rstrip("/") + path_part


def load_site_email() -> str | None:
    """Try to read `email:` from _config.yml without requiring PyYAML."""
    config_path = os.path.join(repo_root(), "_config.yml")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                m = re.match(r"^email:\s*(.+?)\s*$", line)
                if m:
                    val = m.group(1).strip().strip('"').strip("'")
                    return val
    except FileNotFoundError:
        return None
    return None


def repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def parse_post_file(file_path: str) -> tuple[dict[str, str], str]:
    """Parse frontmatter using a small regex approach (no PyYAML needed)."""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Match: ---\n<frontmatter>\n---\n<body>
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, flags=re.S)
    if not m:
        return {}, text

    frontmatter_text = m.group(1)
    body = m.group(2).strip()

    frontmatter: dict[str, str] = {}
    for raw_line in frontmatter_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        kv = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if not kv:
            continue
        key = kv.group(1).strip()
        val = kv.group(2).strip()
        # Strip surrounding quotes
        if len(val) >= 2 and ((val[0] == '"' and val[-1] == '"') or (val[0] == "'" and val[-1] == "'")):
            val = val[1:-1]
        frontmatter[key] = val

    return frontmatter, body


def extract_excerpt(content: str, max_length: int = 300) -> str:
    # Roughly similar to the existing Buttondown script.
    clean = re.sub(r"^#+\s+.*$", "", content, flags=re.MULTILINE)
    clean = re.sub(r"\(.*?\)", "", clean)
    clean = re.sub(r"!\[.*?\]\(.*?\)", "", clean)
    clean = re.sub(r"\[([^\]]*)\]\(.*?\)", r"\1", clean)
    clean = re.sub(r"[*_~`#\[\]]", "", clean)
    clean = re.sub(r"\n\s*\n", "\n\n", clean)

    for line in clean.split("\n"):
        line = line.strip()
        if line and len(line) > 50:
            if len(line) > max_length:
                return line[:max_length] + "..."
            return line
    return ""


def get_confirmed_subscribers(db_path: str) -> list[tuple[str, str]]:
    """Return list of (email, unsubscribe_token) for confirmed subscribers.
    
    Automatically generates a token for any subscriber missing one.
    """
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute(
            "SELECT id, email, unsubscribe_token FROM newsletter_subscribers WHERE confirmed = 1 ORDER BY id"
        )
        rows = cur.fetchall()
        result: list[tuple[str, str]] = []
        for row_id, email, token in rows:
            if not token:
                token = secrets.token_urlsafe(32)
                conn.execute(
                    "UPDATE newsletter_subscribers SET unsubscribe_token = ? WHERE id = ?",
                    (token, row_id)
                )
            result.append((email, token))
        conn.commit()
        return result
    finally:
        conn.close()


def build_unsubscribe_url(unsubscribe_token: str) -> str:
    """Build the full unsubscribe URL for a given token."""
    return TAYIS_BASE_URL.rstrip("/") + "/api/newsletter/unsubscribe?token=" + unsubscribe_token


def build_email(post_file: str, post_url: str, unsubscribe_url: str) -> tuple[str, str, str, str]:
    """Return (subject, text_body, html_body, title, excerpt)."""
    frontmatter, content = parse_post_file(post_file)

    title = frontmatter.get("title") or "New Post"
    author = frontmatter.get("author") or "Tim Lui"

    excerpt = (
        frontmatter.get("excerpt")
        or frontmatter.get("description")
        or extract_excerpt(content)
    )

    subject = "Structure Of Reality - New Post"

    text_body = (
        f"{title}\n\n"
        f"{excerpt}\n\n"
        f"Read the full article: {post_url}\n\n"
        f"---\n"
        f"This email was sent because you subscribed to the Structure of Reality newsletter.\n"
        f"To unsubscribe, visit: {unsubscribe_url}\n"
        f"Written by {author}\n"
    )

    # HTML version with embedded unsubscribe link
    html_body = f"""<html><body>
<p><strong>{title}</strong></p>
<p>{excerpt}</p>
<p><a href="{post_url}">Read the full article</a></p>
<hr>
<p style="font-size:small;color:#666">This email was sent because you subscribed to the Structure of Reality newsletter.<br>
<a href="{unsubscribe_url}">unsubscribe</a><br>
Written by {author}</p>
</body></html>"""

    return subject, text_body, html_body, title, excerpt


def env_flag(name: str, default: bool = False) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "y", "on"}


def main() -> None:
    _load_dotenv()
    parser = argparse.ArgumentParser(description="Send custom newsletter emails via SMTP")
    parser.add_argument("post_file", nargs="?", help="Path to a Jekyll post file (e.g., _posts/2026-01-01-my-post.md)")
    parser.add_argument("post_url", nargs="?", help="Public URL/path to the post (will be re-rooted to the Tayis base URL)")
    parser.add_argument("--latest", action="store_true", default=True, help="Automatically pick the newest _posts/*.md and build its Tayis URL (enabled by default when no args given)")
    parser.add_argument("--no-latest", dest="latest", action="store_false", help="Require explicit post_file and post_url")
    args = parser.parse_args()

    if args.latest:
        if not args.post_file:
            args.post_file = find_latest_post()
        args.post_url = post_to_tayis_url(args.post_file if (args.post_url is None) else args.post_url)
        if args.post_url is None:
            args.post_url = post_to_tayis_url(args.post_file)

    if not args.post_file:
        parser.error("post_file is required when --no-latest is used")

    dry_run = env_flag("DRY_RUN", default=False)

    db_path = os.environ.get(
        "COMMENTS_DB_PATH",
        os.path.join(repo_root(), "comments.db"),
    )
    if not os.path.exists(db_path):
        raise SystemExit(f"comments DB not found: {db_path}")

    post_url = to_tayis_post_url(args.post_url)

    # Load subscribers with tokens
    subscribers = get_confirmed_subscribers(db_path)

    print(f"Post:         {args.post_file}")
    print(f"Public URL:   {post_url}")
    print(f"Subscribers:  {len(subscribers)}")
    print(f"Dry run:      {'YES (no emails will be sent)' if dry_run else 'NO (sending real emails)'}")
    print()

    if not subscribers:
        print("No confirmed subscribers to send to.")
        return

    # Build email content for the first subscriber (used for dry-run display)
    first_email, first_token = subscribers[0]
    unsubscribe_url = build_unsubscribe_url(first_token)
    subject, text_body, html_body, title, excerpt = build_email(args.post_file, post_url, unsubscribe_url)

    print(f"Subject: {subject}")
    print(f"Title:   {title}")
    print(f"Excerpt: {excerpt[:100]}...")
    print(f"--- Body preview ---")
    print(text_body[:500])
    print(f"--- End preview ---")
    print()

    if dry_run:
        print("DRY RUN — no emails were sent.")
        print("Subscriber list with unsubscribe URLs:")
        for email, token in subscribers:
            print(f"  {email} → {build_unsubscribe_url(token)}")
        return

    # --- Real send ---
    smtp_host = os.environ.get("SMTP_HOST")
    if not smtp_host:
        raise SystemExit("SMTP_HOST env is required unless DRY_RUN=1")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_username = os.environ.get("SMTP_USERNAME")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    smtp_use_tls = env_flag("SMTP_USE_TLS", default=True)

    email_from = os.environ.get("EMAIL_FROM") or load_site_email() or "lui.thw@gmail.com"

    print(f"Connecting to SMTP: {smtp_host}:{smtp_port} (TLS={smtp_use_tls})")

    sent_ok = 0
    sent_fail = 0

    with smtplib.SMTP(smtp_host, smtp_port) as smtp:
        smtp.ehlo()
        if smtp_use_tls:
            smtp.starttls()
            smtp.ehlo()

        if smtp_username and smtp_password:
            smtp.login(smtp_username, smtp_password)

        for idx, (recipient, token) in enumerate(subscribers, start=1):
            # Build per-recipient email with their unique unsubscribe link
            unsub_url = build_unsubscribe_url(token)
            _, per_text_body, per_html_body, _, _ = build_email(args.post_file, post_url, unsub_url)

            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = email_from
            msg["To"] = recipient
            msg.set_content(per_text_body)
            msg.add_alternative(per_html_body, subtype="html")

            try:
                smtp.send_message(msg)
                sent_ok += 1
                if idx <= 3 or idx % 25 == 0:
                    print(f"  [{idx}/{len(subscribers)}] sent to {recipient}")
            except Exception as e:
                sent_fail += 1
                print(f"  [{idx}/{len(subscribers)}] FAILED to {recipient}: {e}")

    print("=== Done ===")
    print(f"Sent OK: {sent_ok}")
    print(f"Failed:  {sent_fail}")

    if sent_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
