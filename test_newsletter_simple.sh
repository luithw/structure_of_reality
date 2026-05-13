#!/bin/bash

# Start the server in background
echo "Starting newsletter server..."
python3 comments_server.py &
SERVER_PID=$!
sleep 2

echo ""
echo "✓ Test 1: Subscribe with valid email"
curl -X POST http://localhost:8080/api/newsletter/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}' 2>/dev/null | python3 -m json.tool

echo ""
echo "✓ Test 2: Try duplicate email (should fail)"
curl -X POST http://localhost:8080/api/newsletter/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}' 2>/dev/null | python3 -m json.tool

echo ""
echo "✓ Test 3: Subscribe with another email"
curl -X POST http://localhost:8080/api/newsletter/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"another@example.com"}' 2>/dev/null | python3 -m json.tool

echo ""
echo "✓ Test 4: Invalid email format"
curl -X POST http://localhost:8080/api/newsletter/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"invalid-email"}' 2>/dev/null | python3 -m json.tool

echo ""
echo "✓ Test 5: Check database"
python3 << 'PYEOF'
import sqlite3
conn = sqlite3.connect('comments.db')
subscribers = conn.execute('SELECT id, email, subscribed_at, confirmed FROM newsletter_subscribers').fetchall()
conn.close()
print(f"Total subscribers: {len(subscribers)}")
for sub in subscribers:
    print(f"  - ID: {sub[0]}, Email: {sub[1]}, Confirmed: {sub[3]}")
PYEOF

# Kill the server
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

echo ""
echo "✅ All tests completed!"
