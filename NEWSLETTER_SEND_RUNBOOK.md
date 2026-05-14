---
# Newsletter sending runbook (tracked experiment)

This repo sends newsletter emails via:

- **Script:** `scripts/send_custom_newsletter_notification.py`
- **Subscriber source:** SQLite `comments.db` → table `newsletter_subscribers` (only `confirmed=1`)

## 1) Dry-run (recommended first)
Dry-run renders the email + prints the recipient list, but does **not** send.

**Default — send the latest post (no arguments needed):**

```bash
DRY_RUN=1 python3 scripts/send_custom_newsletter_notification.py
```

**Or specify a post manually:**

```bash
DRY_RUN=1 python3 scripts/send_custom_newsletter_notification.py \
  _posts/2026-04-18-three-ways-to-store-a-note.md \
  "https://tayis.io/u/tim-lui/p/structure-of-reality/2026/04/18/three-ways-to-store-a-note.html"
```

## 2) Real send (after SMTP relay is configured)
The script requires SMTP env vars when `DRY_RUN` is not set.

Set at minimum:
- `SMTP_HOST`

Optionally:
- `SMTP_PORT` (default `587`)
- `SMTP_USERNAME` / `SMTP_PASSWORD` (if your relay requires auth)
- `SMTP_USE_TLS` (default `1` / true)
- `EMAIL_FROM` (optional; defaults from `_config.yml`)

### Gmail SMTP using an App Password (common)
If you want to use your Gmail account as the SMTP relay:

1. Enable **2-Step Verification** on the Google account.
2. Create a **Gmail "App Password"** (from Google Account → Security → App passwords).
3. Use these env vars:

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=1
SMTP_USERNAME=your_gmail_address@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_gmail_address@gmail.com   # recommended
```

> Tip: if `EMAIL_FROM` doesn't match the Gmail account (or isn't added to "Send mail as"), Gmail may reject the message.

For a safe "send to one person" test:
- `NEWSLETTER_TO=you@example.com`

**Default — send the latest post:**

```bash
NEWSLETTER_TO=you@example.com \
SMTP_HOST=smtp.gmail.com SMTP_PORT=587 SMTP_USE_TLS=1 \
SMTP_USERNAME=your_gmail_address@gmail.com SMTP_PASSWORD=your_app_password \
EMAIL_FROM=your_gmail_address@gmail.com \
python3 scripts/send_custom_newsletter_notification.py
```

**Or specify a post manually (with `--no-latest`):**

```bash
NEWSLETTER_TO=you@example.com \
SMTP_HOST=YOUR_SMTP_HOST SMTP_PORT=587 SMTP_USE_TLS=1 \
EMAIL_FROM=you@example.com \
python3 scripts/send_custom_newsletter_notification.py --no-latest \
  _posts/2026-04-18-three-ways-to-store-a-note.md \
  "https://tayis.io/u/tim-lui/p/structure-of-reality/2026/04/18/three-ways-to-store-a-note.html"
```

## 3) How the agent should run this (so you can view logs)
When you want to actually run it, the **Publisher agent must use a tracked experiment**:

- Use `experiment_tool` with `action="run"`
- Put the exact shell command into `command=`
- Use a clear `name=` like `newsletter_custom_send_dry_run_<date>` or `newsletter_custom_send_actual_<date>`

If `SMTP_HOST` is missing, the script will exit with:
> `SMTP_HOST is required unless DRY_RUN=1`
---
