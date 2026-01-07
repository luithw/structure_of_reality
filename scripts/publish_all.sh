#!/bin/bash
# Publish a blog post to all platforms
#
# Usage: ./publish_all.sh <post_file.md>

set -e

if [ $# -lt 1 ]; then
    echo "Usage: ./publish_all.sh <post_file.md>"
    exit 1
fi

POST_FILE="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check if post file exists
if [ ! -f "$POST_FILE" ]; then
    echo "Error: Post file not found: $POST_FILE"
    exit 1
fi

# Extract post date and title from filename (assuming Jekyll format: YYYY-MM-DD-title.md)
FILENAME=$(basename "$POST_FILE")
POST_DATE=$(echo "$FILENAME" | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}')
POST_SLUG=$(echo "$FILENAME" | sed -E 's/^[0-9]{4}-[0-9]{2}-[0-9]{2}-(.*)\.md$/\1/')

# Construct the GitHub Pages URL
if [ -n "$GITHUB_PAGES_URL" ]; then
    BASE_URL="$GITHUB_PAGES_URL"
else
    # Fallback to default (user should set this)
    BASE_URL="${GITHUB_PAGES_URL:-https://yourusername.github.io/structure_of_reality}"
fi

# Convert date to URL format (YYYY/MM/DD)
YEAR=$(echo "$POST_DATE" | cut -d'-' -f1)
MONTH=$(echo "$POST_DATE" | cut -d'-' -f2)
DAY=$(echo "$POST_DATE" | cut -d'-' -f3)

POST_URL="${BASE_URL}/${YEAR}/${MONTH}/${DAY}/${POST_SLUG}/"

echo "=========================================="
echo "Publishing Post"
echo "=========================================="
echo "File: $POST_FILE"
echo "URL: $POST_URL"
echo ""

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv "$SCRIPT_DIR/venv"
    source "$SCRIPT_DIR/venv/bin/activate"
    pip install -r "$SCRIPT_DIR/requirements.txt"
else
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# Publish to Facebook
echo "=========================================="
echo "Publishing to Facebook..."
echo "=========================================="
if python3 "$SCRIPT_DIR/publish_to_facebook.py" "$POST_FILE" "$POST_URL"; then
    echo "✅ Published to Facebook"
else
    echo "⚠️  Failed to publish to Facebook"
fi

echo ""
echo "=========================================="
echo "Publishing Complete!"
echo "=========================================="
echo "Your post is now available at:"
echo "  GitHub Pages: $POST_URL"
echo ""
echo "Remember to commit and push the changes to GitHub!"

deactivate

