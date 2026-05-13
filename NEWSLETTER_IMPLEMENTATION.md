# Custom Newsletter Implementation

## Overview
Replaced Buttondown newsletter integration with a custom backend solution that mirrors the comments API architecture.

## Changes Made

### 1. Backend API (`comments_server.py`)
Added newsletter subscription endpoint to the existing comments server:

**Endpoint:** `POST /api/newsletter/subscribe`
- **Request:** `{ "email": "user@example.com" }`
- **Response (201):** `{ "id": 1, "email": "user@example.com", "subscribed_at": 1234567890, "message": "Successfully subscribed to newsletter!" }`
- **Error (409):** `{ "error": "email already subscribed" }` - if email exists
- **Error (400):** `{ "error": "invalid email" }` - if email format is invalid

**Database:** Uses SQLite `newsletter_subscribers` table with:
- `id` (INTEGER PRIMARY KEY)
- `email` (TEXT UNIQUE)
- `subscribed_at` (INTEGER timestamp)
- `confirmed` (INTEGER, default 0)

### 2. Frontend Form (`_layouts/default.html`)
Replaced Buttondown form with custom HTML form:

```html
<form class="newsletter-form" id="newsletter-form">
    <input type="email" id="newsletter-email" name="email" placeholder="Enter your email" required>
    <button type="submit">Subscribe</button>
</form>
```

### 3. Frontend JavaScript
Implemented client-side handler that:
- Validates email format
- Sends POST request to `/api/newsletter/subscribe` using relative path
- Handles success/error responses
- Shows user feedback messages
- Auto-hides success message after 5 seconds

**Key Features:**
- Uses relative paths (no hardcoded domain)
- Dynamically calculates API base URL from current page path
- Handles subpath deployments (e.g., `/u/tim-lui/p/...`)
- CORS-enabled backend

### 4. Updated Files
- `comments_server.py` - Added newsletter table and POST endpoint
- `_layouts/default.html` - Replaced Buttondown form with custom form + JavaScript
- All 9 HTML files in `_site/` - Updated with new newsletter form

## API Usage Pattern

The implementation follows the same pattern as the comments API:

```javascript
// Calculate API base from current path
const pathParts = window.location.pathname.split('/').filter(p => p);
let apiBase = '/';

// Make request with relative path
fetch(apiBase + 'api/newsletter/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email })
})
```

## Database Schema

```sql
CREATE TABLE newsletter_subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    subscribed_at INTEGER NOT NULL,
    confirmed INTEGER DEFAULT 0
);

CREATE INDEX idx_newsletter_email ON newsletter_subscribers(email);
```

## Testing

To test the newsletter subscription:

1. Start the comments server (if not already running)
2. Navigate to any page with the newsletter form
3. Enter an email address and click "Subscribe"
4. Check the response in browser console
5. Verify email is stored in `comments.db` using:
   ```sql
   SELECT * FROM newsletter_subscribers;
   ```

## Future Enhancements

- Email confirmation flow (set `confirmed = 1` after verification)
- Unsubscribe endpoint: `DELETE /api/newsletter/subscribe/{email}`
- Get subscribers list: `GET /api/newsletter/subscribers` (admin only)
- Integration with email service to send notifications on new posts
- Subscriber count endpoint: `GET /api/newsletter/count`

## Migration from Buttondown

All existing Buttondown functionality has been removed:
- No external API calls
- No popup windows
- No dependency on Buttondown service
- All data stored locally in SQLite

To migrate existing subscribers from Buttondown:
1. Export subscriber list from Buttondown
2. Import into `newsletter_subscribers` table with `confirmed = 1`
