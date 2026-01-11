# Features Setup Guide

This document explains how to set up all the interactive features for your blog.

## Table of Contents

1. [Comment System (Utterances)](#1-comment-system-utterances)
2. [User Accounts (Firebase Auth)](#2-user-accounts-firebase-auth)
3. [Newsletter Subscription (Buttondown)](#3-newsletter-subscription-buttondown)
4. [Auto Email Notifications](#4-auto-email-notifications)
5. [SMS & WhatsApp Alerts (Twilio)](#5-sms--whatsapp-alerts-twilio)

---

## 1. Comment System (Utterances)

Utterances is a lightweight commenting system built on GitHub Issues. Readers sign in with GitHub to comment.

### Setup Steps:

1. **Install Utterances App**
   - Go to [utteranc.es](https://utteranc.es/)
   - Click "Install" and add it to your repository (`luithw/structure_of_reality`)

2. **Configure in `_config.yml`**
   ```yaml
   github_repo: luithw/structure_of_reality
   ```

3. **That's it!** Comments will appear at the bottom of each post.

### How it works:
- Each blog post creates a GitHub Issue when someone comments
- Comments are stored as issue comments
- Readers must sign in with GitHub to comment
- You can moderate comments directly from GitHub Issues

---

## 2. User Accounts (Firebase Auth)

Firebase Authentication provides a secure, scalable user authentication system.

### Setup Steps:

1. **Create Firebase Project**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Click "Add project" and follow the wizard
   - Enable Google Analytics (optional)

2. **Enable Authentication**
   - In your project, go to "Authentication" → "Sign-in method"
   - Enable "Email/Password"
   - Enable "Google" (for Google Sign-In)

3. **Add Your Domain**
   - Go to "Authentication" → "Settings" → "Authorized domains"
   - Add your domain: `luithw.github.io`

4. **Get Config Values**
   - Go to "Project settings" (gear icon)
   - Under "Your apps", click the web icon `</>`
   - Copy the config values

5. **Update `_config.yml`**
   ```yaml
   firebase_api_key: AIzaSy...
   firebase_auth_domain: your-project.firebaseapp.com
   firebase_project_id: your-project-id
   firebase_storage_bucket: your-project.appspot.com
   firebase_messaging_sender_id: 123456789
   firebase_app_id: 1:123456789:web:abc123
   ```

### Features:
- Email/password sign up and sign in
- Google Sign-In with one click
- User session persists across visits
- Sign out functionality

---

## 3. Newsletter Subscription (Buttondown)

Buttondown is a simple, privacy-focused newsletter service.

### Setup Steps:

1. **Create Buttondown Account**
   - Go to [buttondown.email](https://buttondown.email/)
   - Sign up for free (up to 100 subscribers free)

2. **Choose Your Username**
   - Your newsletter URL will be: `buttondown.email/your-username`

3. **Update `_config.yml`**
   ```yaml
   buttondown_username: your-username
   ```

4. **Get API Key (for auto-emails)**
   - Go to [Settings → Programming](https://buttondown.email/settings/programming)
   - Copy your API key

5. **Add to GitHub Secrets**
   - Go to your repo → Settings → Secrets and variables → Actions
   - Add secret: `BUTTONDOWN_API_KEY`

### Features:
- Embedded signup form in footer
- Subscribers automatically receive new post emails
- Simple, clean email templates
- Easy to manage subscriber list

---

## 4. Auto Email Notifications

Automatically send emails to all newsletter subscribers when you publish a new post.

### Setup Steps:

1. **Complete Buttondown setup** (see above)

2. **Add GitHub Secret**
   - Repository → Settings → Secrets and variables → Actions
   - New repository secret:
     - Name: `BUTTONDOWN_API_KEY`
     - Value: Your Buttondown API key

3. **How it works:**
   - When you push a new post to `_posts/`
   - GitHub Actions workflow runs
   - Email is automatically sent to all subscribers

### Email Content:
- Subject: "📝 New Post: [Post Title]"
- Body: Post excerpt with link to full article

---

## 5. SMS & WhatsApp Alerts (Twilio)

Get instant text/WhatsApp notifications when a new post is published.

### Setup Steps:

1. **Create Twilio Account**
   - Go to [twilio.com](https://www.twilio.com/)
   - Sign up (free trial includes credits)

2. **Get Credentials**
   - Dashboard → Account SID
   - Dashboard → Auth Token

3. **For SMS:**
   - Buy a phone number ($1/month)
   - Go to "Phone Numbers" → "Buy a Number"

4. **For WhatsApp:**
   - Go to "Messaging" → "Try it out" → "Send a WhatsApp message"
   - Save the sandbox number: `+14155238886`
   - Send "join <your-sandbox-code>" to this number from your phone

5. **Add GitHub Secrets:**
   
   | Secret Name | Value |
   |------------|-------|
   | `TWILIO_ACCOUNT_SID` | Your Account SID |
   | `TWILIO_AUTH_TOKEN` | Your Auth Token |
   | `TWILIO_PHONE_NUMBER` | Your Twilio number (e.g., `+1234567890`) |
   | `TWILIO_WHATSAPP_NUMBER` | `+14155238886` (sandbox) |
   | `NOTIFICATION_PHONE_NUMBERS` | Your phone(s) comma-separated (e.g., `+1234567890,+0987654321`) |

6. **Add GitHub Variable:**
   - Go to Settings → Secrets and variables → Actions → Variables
   - Add variable:
     - Name: `NOTIFICATION_CHANNELS`
     - Value: `sms,whatsapp` (or just `sms` or `whatsapp`)

### Message Format:
```
📝 New Blog Post Published!

[Post Title]

Read it here: [URL]

- Structure of Reality
```

---

## Summary of Required Secrets

Add these to your GitHub repository (Settings → Secrets → Actions):

### Required for all features:
| Secret | Used For |
|--------|----------|
| `BUTTONDOWN_API_KEY` | Email notifications |
| `TWILIO_ACCOUNT_SID` | SMS/WhatsApp |
| `TWILIO_AUTH_TOKEN` | SMS/WhatsApp |
| `TWILIO_PHONE_NUMBER` | SMS sending |
| `TWILIO_WHATSAPP_NUMBER` | WhatsApp sending |
| `NOTIFICATION_PHONE_NUMBERS` | Recipients |

### Variables (not secrets):
| Variable | Value |
|----------|-------|
| `PAGES_URL` | `https://luithw.github.io/structure_of_reality` |
| `NOTIFICATION_CHANNELS` | `sms,whatsapp` |

---

## Testing Locally

### Test Email Script:
```bash
export BUTTONDOWN_API_KEY="your-key"
python scripts/send_email_notification.py _posts/your-post.md "https://example.com/post-url"
```

### Test SMS Script:
```bash
export TWILIO_ACCOUNT_SID="your-sid"
export TWILIO_AUTH_TOKEN="your-token"
export TWILIO_PHONE_NUMBER="+1234567890"
export NOTIFICATION_PHONE_NUMBERS="+1234567890"
export NOTIFICATION_CHANNELS="sms"
python scripts/send_sms_notification.py _posts/your-post.md "https://example.com/post-url"
```

---

## Troubleshooting

### Comments not showing:
- Make sure Utterances app is installed on your repo
- Check that `github_repo` in `_config.yml` is correct
- Verify the repo is public

### Firebase auth not working:
- Check that your domain is in authorized domains
- Verify all config values are correct
- Check browser console for errors

### Emails not sending:
- Verify `BUTTONDOWN_API_KEY` is set correctly
- Check GitHub Actions logs for errors
- Make sure you have at least one subscriber

### SMS/WhatsApp not sending:
- Verify all Twilio credentials
- For WhatsApp: make sure you've joined the sandbox
- Check phone number format (must include country code with +)
