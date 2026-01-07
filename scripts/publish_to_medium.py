#!/usr/bin/env python3
"""
Script to publish a blog post to Medium.

Requirements:
- Medium Integration Token (get from https://medium.com/me/settings)
- Post should be in markdown format

Usage:
    python publish_to_medium.py <post_file.md>
"""

import os
import sys
import json
import requests
import yaml
import markdown2
from datetime import datetime


class MediumPublisher:
    def __init__(self, integration_token):
        self.integration_token = integration_token
        self.api_base = "https://api.medium.com/v1"
        self.headers = {
            "Authorization": f"Bearer {integration_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def get_user_info(self):
        """Get authenticated user's information."""
        response = requests.get(f"{self.api_base}/me", headers=self.headers)
        response.raise_for_status()
        return response.json()["data"]
    
    def create_post(self, user_id, title, content, tags=None, publish_status="public", 
                    canonical_url=None, content_format="markdown"):
        """
        Create a new post on Medium.
        
        Args:
            user_id: The user's Medium ID
            title: Post title
            content: Post content (markdown or HTML)
            tags: List of tags (max 3)
            publish_status: "public", "draft", or "unlisted"
            canonical_url: Original URL (for cross-posting)
            content_format: "markdown" or "html"
        """
        data = {
            "title": title,
            "contentFormat": content_format,
            "content": content,
            "publishStatus": publish_status
        }
        
        if tags:
            data["tags"] = tags[:3]  # Medium allows max 3 tags
        
        if canonical_url:
            data["canonicalUrl"] = canonical_url
        
        response = requests.post(
            f"{self.api_base}/users/{user_id}/posts",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()["data"]


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
    if len(sys.argv) < 2:
        print("Usage: python publish_to_medium.py <post_file.md>")
        sys.exit(1)
    
    post_file = sys.argv[1]
    
    # Get Medium integration token from environment
    integration_token = os.environ.get("MEDIUM_INTEGRATION_TOKEN")
    if not integration_token:
        print("Error: MEDIUM_INTEGRATION_TOKEN environment variable not set")
        print("Get your token from: https://medium.com/me/settings")
        sys.exit(1)
    
    # Parse post file
    try:
        frontmatter, content = parse_post_file(post_file)
    except Exception as e:
        print(f"Error reading post file: {e}")
        sys.exit(1)
    
    # Extract metadata
    title = frontmatter.get("title", "Untitled")
    tags = frontmatter.get("tags", [])
    publish_status = frontmatter.get("medium_status", "public")
    canonical_url = frontmatter.get("canonical_url")
    
    # Add a note about cross-posting
    if canonical_url:
        content = f"*Originally published at [{canonical_url}]({canonical_url})*\n\n---\n\n{content}"
    
    # Initialize publisher
    publisher = MediumPublisher(integration_token)
    
    try:
        # Get user info
        print("Authenticating with Medium...")
        user_info = publisher.get_user_info()
        print(f"Authenticated as: {user_info['name']} (@{user_info['username']})")
        
        # Create post
        print(f"\nPublishing post: {title}")
        result = publisher.create_post(
            user_id=user_info["id"],
            title=title,
            content=content,
            tags=tags,
            publish_status=publish_status,
            canonical_url=canonical_url,
            content_format="markdown"
        )
        
        print(f"\n✅ Successfully published to Medium!")
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Status: {result['publishStatus']}")
        
        # Save the Medium URL back to the post file
        if "medium_url" not in frontmatter:
            update_post_with_medium_url(post_file, result["url"])
        
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ Error publishing to Medium: {e}")
        print(f"Response: {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def update_post_with_medium_url(post_file, medium_url):
    """Update the post file to include the Medium URL."""
    try:
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                # Add medium_url to frontmatter
                frontmatter += f"\nmedium_url: {medium_url}"
                new_content = f"---{frontmatter}---{parts[2]}"
                
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"\n📝 Updated post file with Medium URL")
    except Exception as e:
        print(f"Warning: Could not update post file with Medium URL: {e}")


if __name__ == "__main__":
    main()

