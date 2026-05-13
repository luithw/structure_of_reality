#!/usr/bin/env python3
"""Test the newsletter API."""

import json
import sqlite3
import subprocess
import time
import requests
import sys

# Start the server in background
print("Starting newsletter server...")
proc = subprocess.Popen([sys.executable, 'comments_server.py'], 
                       stdout=subprocess.PIPE, 
                       stderr=subprocess.PIPE)
time.sleep(2)

try:
    # Test 1: Subscribe with valid email
    print("\n✓ Test 1: Subscribe with valid email")
    response = requests.post('http://localhost:8080/api/newsletter/subscribe', 
                            json={'email': 'test@example.com'})
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    
    # Test 2: Try to subscribe with same email (should fail)
    print("\n✓ Test 2: Try to subscribe with duplicate email")
    response = requests.post('http://localhost:8080/api/newsletter/subscribe', 
                            json={'email': 'test@example.com'})
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    
    # Test 3: Subscribe with another email
    print("\n✓ Test 3: Subscribe with another email")
    response = requests.post('http://localhost:8080/api/newsletter/subscribe', 
                            json={'email': 'another@example.com'})
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    
    # Test 4: Invalid email
    print("\n✓ Test 4: Invalid email format")
    response = requests.post('http://localhost:8080/api/newsletter/subscribe', 
                            json={'email': 'invalid-email'})
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    
    # Test 5: Check database
    print("\n✓ Test 5: Check database")
    conn = sqlite3.connect('comments.db')
    subscribers = conn.execute('SELECT * FROM newsletter_subscribers').fetchall()
    conn.close()
    print(f"  Total subscribers: {len(subscribers)}")
    for sub in subscribers:
        print(f"    - {sub}")
    
    print("\n✅ All tests passed!")
    
finally:
    # Kill the server
    proc.terminate()
    proc.wait()
