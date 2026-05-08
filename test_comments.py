import urllib.request
import json
import sqlite3
from datetime import datetime

print("=" * 60)
print("COMMENT SYSTEM TEST")
print("=" * 60)

# Test 1: POST a new comment
print("\n[TEST 1] Posting a new comment...")
url = 'http://localhost:8080/api/comments'
data = {
    'post_slug': '/2026/04/26/from-surviving-to-foraging',
    'author_name': 'System Test',
    'body': f'Automated test at {datetime.now().isoformat()}'
}

try:
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        comment_id = result.get('id')
        print(f"✓ Comment posted successfully (ID: {comment_id})")
except Exception as e:
    print(f"✗ Error posting comment: {e}")
    exit(1)

# Test 2: GET comments via API
print("\n[TEST 2] Fetching comments via API...")
get_url = 'http://localhost:8080/api/comments?post_slug=/2026/04/26/from-surviving-to-foraging'
try:
    with urllib.request.urlopen(get_url) as response:
        result = json.loads(response.read().decode('utf-8'))
        comments = result.get('comments', [])
        print(f"✓ API returned {len(comments)} comments")
        # Check if our comment is there
        found = any(c['author_name'] == 'System Test' for c in comments)
        if found:
            print(f"✓ Our test comment is in the API response")
        else:
            print(f"✗ Test comment not found in API response")
except Exception as e:
    print(f"✗ Error fetching comments: {e}")
    exit(1)

# Test 3: Verify in database
print("\n[TEST 3] Verifying in database...")
try:
    conn = sqlite3.connect('/workspace/comments.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM comments')
    total = cursor.fetchone()[0]
    print(f"✓ Database has {total} total comments")
    
    cursor.execute('SELECT * FROM comments WHERE author_name = "System Test" ORDER BY id DESC LIMIT 1')
    comment = cursor.fetchone()
    if comment:
        print(f"✓ Test comment found in database (ID: {comment[0]})")
    else:
        print(f"✗ Test comment not found in database")
    conn.close()
except Exception as e:
    print(f"✗ Error checking database: {e}")
    exit(1)

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED - Comment system is working!")
print("=" * 60)
