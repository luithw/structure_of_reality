#!/usr/bin/env python3
"""
Script to send SMS and WhatsApp notifications when a new post is published.

Uses Twilio API for both SMS and WhatsApp messages.

Requirements:
- Twilio Account SID and Auth Token
- Twilio Phone Number (for SMS)
- Twilio WhatsApp Number (for WhatsApp)

Usage:
    python send_sms_notification.py <post_file.md> <github_pages_url>

Environment Variables:
    TWILIO_ACCOUNT_SID: Your Twilio Account SID
    TWILIO_AUTH_TOKEN: Your Twilio Auth Token
    TWILIO_PHONE_NUMBER: Your Twilio phone number (e.g., +1234567890)
    TWILIO_WHATSAPP_NUMBER: Twilio WhatsApp number (e.g., +14155238886)
    NOTIFICATION_PHONE_NUMBERS: Comma-separated phone numbers to notify (e.g., +1234567890,+0987654321)
    NOTIFICATION_CHANNELS: Comma-separated channels to use (sms,whatsapp)
"""

import os
import sys
import json
import yaml
from datetime import datetime

try:
    from twilio.rest import Client
except ImportError:
    print("Twilio library not installed. Run: pip install twilio")
    sys.exit(1)


class TwilioNotifier:
    """Send SMS and WhatsApp messages via Twilio."""
    
    def __init__(self, account_sid, auth_token, phone_number, whatsapp_number=None):
        self.client = Client(account_sid, auth_token)
        self.phone_number = phone_number
        self.whatsapp_number = whatsapp_number or "whatsapp:+14155238886"  # Twilio sandbox default
    
    def send_sms(self, to_number, message):
        """
        Send an SMS message.
        
        Args:
            to_number: Recipient phone number (e.g., +1234567890)
            message: Message text (max 1600 chars, will be split if longer)
        """
        # Ensure proper format
        if not to_number.startswith('+'):
            to_number = '+' + to_number
        
        msg = self.client.messages.create(
            body=message[:1600],  # SMS limit
            from_=self.phone_number,
            to=to_number
        )
        return msg
    
    def send_whatsapp(self, to_number, message):
        """
        Send a WhatsApp message.
        
        Args:
            to_number: Recipient phone number (e.g., +1234567890)
            message: Message text
        
        Note: For WhatsApp, recipients must have opted in by sending a message
        to your Twilio WhatsApp number first.
        """
        # Ensure proper format
        if not to_number.startswith('+'):
            to_number = '+' + to_number
        
        # WhatsApp requires 'whatsapp:' prefix
        from_whatsapp = self.whatsapp_number
        if not from_whatsapp.startswith('whatsapp:'):
            from_whatsapp = f"whatsapp:{from_whatsapp}"
        
        to_whatsapp = f"whatsapp:{to_number}"
        
        msg = self.client.messages.create(
            body=message,
            from_=from_whatsapp,
            to=to_whatsapp
        )
        return msg


def parse_post_file(file_path):
    """Parse a Jekyll post file and extract frontmatter and content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            markdown_content = parts[2].strip()
        else:
            frontmatter = {}
            markdown_content = content
    else:
        frontmatter = {}
        markdown_content = content
    
    return frontmatter, markdown_content


def main():
    if len(sys.argv) < 3:
        print("Usage: python send_sms_notification.py <post_file.md> <github_pages_url>")
        sys.exit(1)
    
    post_file = sys.argv[1]
    post_url = sys.argv[2]
    
    # Get Twilio credentials from environment
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
    whatsapp_number = os.environ.get("TWILIO_WHATSAPP_NUMBER")
    
    # Get notification settings
    notification_numbers = os.environ.get("NOTIFICATION_PHONE_NUMBERS", "")
    channels = os.environ.get("NOTIFICATION_CHANNELS", "sms,whatsapp")
    
    if not account_sid or not auth_token:
        print("Error: Twilio credentials not set")
        print("Required environment variables:")
        print("  - TWILIO_ACCOUNT_SID")
        print("  - TWILIO_AUTH_TOKEN")
        print("  - TWILIO_PHONE_NUMBER (for SMS)")
        print("  - TWILIO_WHATSAPP_NUMBER (for WhatsApp, optional)")
        print("  - NOTIFICATION_PHONE_NUMBERS (comma-separated)")
        print("  - NOTIFICATION_CHANNELS (sms,whatsapp)")
        sys.exit(1)
    
    if not notification_numbers:
        print("Warning: No notification phone numbers configured")
        print("Set NOTIFICATION_PHONE_NUMBERS environment variable")
        sys.exit(0)
    
    # Parse post file
    try:
        frontmatter, content = parse_post_file(post_file)
    except Exception as e:
        print(f"Error reading post file: {e}")
        sys.exit(1)
    
    # Extract metadata
    title = frontmatter.get("title", "New Post")
    
    # Create notification message
    message = f"""📝 New Blog Post Published!

{title}

Read it here: {post_url}

- Structure of Reality"""
    
    # Initialize notifier
    notifier = TwilioNotifier(account_sid, auth_token, phone_number, whatsapp_number)
    
    # Parse channels and numbers
    channel_list = [c.strip().lower() for c in channels.split(',')]
    number_list = [n.strip() for n in notification_numbers.split(',') if n.strip()]
    
    print(f"Sending notifications for: {title}")
    print(f"Channels: {', '.join(channel_list)}")
    print(f"Recipients: {len(number_list)} number(s)")
    
    success_count = 0
    error_count = 0
    
    for number in number_list:
        for channel in channel_list:
            try:
                if channel == 'sms':
                    if not phone_number:
                        print(f"  ⚠️  SMS skipped (no Twilio phone number configured)")
                        continue
                    result = notifier.send_sms(number, message)
                    print(f"  ✅ SMS sent to {number} (SID: {result.sid})")
                    success_count += 1
                    
                elif channel == 'whatsapp':
                    result = notifier.send_whatsapp(number, message)
                    print(f"  ✅ WhatsApp sent to {number} (SID: {result.sid})")
                    success_count += 1
                    
                else:
                    print(f"  ⚠️  Unknown channel: {channel}")
                    
            except Exception as e:
                print(f"  ❌ Failed to send {channel} to {number}: {e}")
                error_count += 1
    
    print(f"\n📊 Summary: {success_count} sent, {error_count} failed")
    
    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
