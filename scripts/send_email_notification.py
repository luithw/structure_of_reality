#!/usr/bin/env python3
"""
Script to send email notifications to subscribers when a new post is published.

This script integrates with Buttondown API to send email notifications.
Buttondown will automatically send emails to all your subscribers.

Requirements:
- Buttondown API Key (get from buttondown.email dashboard)

Usage:
    python send_email_notification.py <post_file.md> <github_pages_url>

Environment Variables:
    BUTTONDOWN_API_KEY: Your Buttondown API key
"""

import os
import sys
import json
import requests
import yaml
from datetime import datetime


class ButtondownEmailer:
    """Send emails via Buttondown API."""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_base = "https://api.buttondown.email/v1"
        self.headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json"
        }
    
    def send_email(self, subject, body, email_type="public"):
        """
        Create and send a new email to all subscribers.
        
        Args:
            subject: Email subject line
            body: Email body in Markdown format
            email_type: 'public' (newsletter), 'private' (not in archives)
        """
        endpoint = f"{self.api_base}/emails"
        
        data = {
            "subject": subject,
            "body": body,
            "status": "sent",  # 'sent' to send immediately, 'draft' to save
            "email_type": email_type
        }
        
        response = requests.post(endpoint, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_subscribers_count(self):
        """Get the number of active subscribers."""
        endpoint = f"{self.api_base}/subscribers"
        params = {"type": "regular"}
        
        response = requests.get(endpoint, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("count", 0)


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


def extract_excerpt(content, max_length=300):
    """Extract a short excerpt from the content."""
    # Remove markdown formatting
    content = content.replace('#', '').replace('*', '').replace('_', '')
    lines = content.split('\n')
    
    # Get first meaningful paragraph
    for line in lines:
        line = line.strip()
        if line and len(line) > 50:
            if len(line) > max_length:
                return line[:max_length] + "..."
            return line
    
    return ""


def main():
    if len(sys.argv) < 3:
        print("Usage: python send_email_notification.py <post_file.md> <github_pages_url>")
        sys.exit(1)
    
    post_file = sys.argv[1]
    post_url = sys.argv[2]
    
    # Get Buttondown API key from environment
    api_key = os.environ.get("BUTTONDOWN_API_KEY")
    
    if not api_key:
        print("Error: BUTTONDOWN_API_KEY not set")
        print("Get your API key from: https://buttondown.email/settings/programming")
        sys.exit(1)
    
    # Parse post file
    try:
        frontmatter, content = parse_post_file(post_file)
    except Exception as e:
        print(f"Error reading post file: {e}")
        sys.exit(1)
    
    # Extract metadata
    title = frontmatter.get("title", "New Post")
    excerpt = frontmatter.get("excerpt") or extract_excerpt(content)
    author = frontmatter.get("author", "Tim Lui")
    
    # Create email content
    subject = f"📝 New Post: {title}"
    
    email_body = f"""# {title}

{excerpt}

---

**[Read the full article →]({post_url})**

---

*This email was sent because you subscribed to Structure of Reality newsletter.*

*Written by {author}*
"""
    
    # Initialize emailer
    emailer = ButtondownEmailer(api_key)
    
    try:
        # Get subscriber count
        subscriber_count = emailer.get_subscribers_count()
        print(f"Sending notification to {subscriber_count} subscribers...")
        
        # Send email
        result = emailer.send_email(subject, email_body)
        
        print(f"\n✅ Successfully sent email notification!")
        print(f"Email ID: {result.get('id', 'N/A')}")
        print(f"Subject: {subject}")
        print(f"Recipients: {subscriber_count} subscribers")
        
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ Error sending email: {e}")
        try:
            error_data = e.response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Response: {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
