#!/usr/bin/env python3
"""
Script to publish a blog post link to Facebook.

Requirements:
- Facebook Page Access Token (get from Facebook Developer Console)
- Facebook Page ID

Usage:
    python publish_to_facebook.py <post_file.md> <github_pages_url>
"""

import os
import sys
import json
import requests
import yaml
from datetime import datetime


class FacebookPublisher:
    def __init__(self, access_token, page_id):
        self.access_token = access_token
        self.page_id = page_id
        self.api_base = "https://graph.facebook.com/v18.0"
    
    def publish_link(self, link, message="", published=True):
        """
        Publish a link to Facebook page.
        
        Args:
            link: URL to share
            message: Text to accompany the link
            published: Whether to publish immediately or save as draft
        """
        endpoint = f"{self.api_base}/{self.page_id}/feed"
        
        data = {
            "link": link,
            "message": message,
            "published": published,
            "access_token": self.access_token
        }
        
        response = requests.post(endpoint, data=data)
        response.raise_for_status()
        return response.json()
    
    def get_page_info(self):
        """Get page information."""
        endpoint = f"{self.api_base}/{self.page_id}"
        params = {
            "fields": "name,username,about",
            "access_token": self.access_token
        }
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()


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


def extract_excerpt(content, max_length=200):
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
    
    # Fallback to first non-empty line
    for line in lines:
        line = line.strip()
        if line:
            if len(line) > max_length:
                return line[:max_length] + "..."
            return line
    
    return ""


def main():
    if len(sys.argv) < 3:
        print("Usage: python publish_to_facebook.py <post_file.md> <github_pages_url>")
        sys.exit(1)
    
    post_file = sys.argv[1]
    post_url = sys.argv[2]
    
    # Get Facebook credentials from environment
    access_token = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN")
    page_id = os.environ.get("FACEBOOK_PAGE_ID")
    
    if not access_token or not page_id:
        print("Error: Facebook credentials not set")
        print("Required environment variables:")
        print("  - FACEBOOK_PAGE_ACCESS_TOKEN")
        print("  - FACEBOOK_PAGE_ID")
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
    
    # Create Facebook message
    message = f"{title}\n\n{excerpt}\n\nRead more at: {post_url}"
    
    # Initialize publisher
    publisher = FacebookPublisher(access_token, page_id)
    
    try:
        # Get page info
        print("Authenticating with Facebook...")
        page_info = publisher.get_page_info()
        print(f"Publishing to page: {page_info['name']}")
        
        # Publish post
        print(f"\nPublishing post: {title}")
        result = publisher.publish_link(
            link=post_url,
            message=message,
            published=True
        )
        
        print(f"\n✅ Successfully published to Facebook!")
        print(f"Post ID: {result['id']}")
        print(f"View at: https://www.facebook.com/{result['id']}")
        
        # Save the Facebook post ID
        if "facebook_post_id" not in frontmatter:
            update_post_with_facebook_id(post_file, result["id"])
        
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ Error publishing to Facebook: {e}")
        try:
            error_data = e.response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Response: {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def update_post_with_facebook_id(post_file, facebook_id):
    """Update the post file to include the Facebook post ID."""
    try:
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                # Add facebook_post_id to frontmatter
                frontmatter += f"\nfacebook_post_id: {facebook_id}"
                new_content = f"---{frontmatter}---{parts[2]}"
                
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"\n📝 Updated post file with Facebook post ID")
    except Exception as e:
        print(f"Warning: Could not update post file with Facebook ID: {e}")


if __name__ == "__main__":
    main()

