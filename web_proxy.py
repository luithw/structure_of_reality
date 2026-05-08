#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import urllib.error
import os
import sys
from urllib.parse import urlparse

class ProxyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # First try _site directory
        parsed = urlparse(path)
        filepath = parsed.path.lstrip('/')
        
        # Check if file exists in _site
        if os.path.exists(os.path.join('_site', filepath)):
            return os.path.join('_site', filepath)
        # Otherwise serve from workspace root
        return filepath
    
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path.startswith('/api/'):
            self.proxy_request()
        else:
            super().do_GET()
    
    def do_POST(self):
        parsed = urlparse(self.path)
        
        if parsed.path.startswith('/api/'):
            self.proxy_request()
        else:
            self.send_response(405)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def proxy_request(self):
        try:
            url = f'http://localhost:8080{self.path}'
            print(f'[PROXY] {self.command} {self.path}', file=sys.stderr)
            
            if self.command == 'POST':
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json'})
            else:
                req = urllib.request.Request(url)
            
            r = urllib.request.urlopen(req)
            response_data = r.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(response_data)))
            self.end_headers()
            self.wfile.write(response_data)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
        except Exception as e:
            print(f'[PROXY] Error: {e}', file=sys.stderr)
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 4000), ProxyHTTPRequestHandler)
    print('Web server running on port 4000', file=sys.stderr)
    server.serve_forever()
