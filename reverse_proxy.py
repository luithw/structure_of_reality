#!/usr/bin/env python3
"""Reverse proxy that serves static files and forwards /api requests to comments backend."""

import os
import sys
import http.server
import socketserver
import urllib.request
import urllib.error
from urllib.parse import urlparse

class ReverseProxyHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        """Override to serve from _site directory."""
        # Remove leading slash and serve from _site
        if path.startswith('/'):
            path = path[1:]
        return os.path.join('_site', path)
    
    def do_GET(self):
        if self.path.startswith('/api/'):
            self._proxy_request('GET')
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            self._proxy_request('POST')
        else:
            self.send_error(405)
    
    def do_OPTIONS(self):
        if self.path.startswith('/api/'):
            self._proxy_request('OPTIONS')
        else:
            self.send_error(405)
    
    def _proxy_request(self, method):
        """Forward request to comments backend."""
        target_url = 'http://localhost:8080' + self.path
        
        try:
            # Read request body if present
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            # Create request
            req = urllib.request.Request(
                target_url,
                data=body,
                method=method
            )
            
            # Copy relevant headers
            for header, value in self.headers.items():
                if header.lower() not in ['host', 'content-length']:
                    req.add_header(header, value)
            
            # Forward request
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                for header, value in response.headers.items():
                    self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())
        
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"error": "Backend error"}')
        except Exception as e:
            print(f'Proxy error: {e}', file=sys.stderr)
            self.send_error(502, 'Bad Gateway')
    
    def log_message(self, format, *args):
        """Log requests."""
        print(f'{self.client_address[0]} - {format % args}')

class ReuseAddrTCPServer(socketserver.TCPServer):
    """TCP server that allows address reuse."""
    allow_reuse_address = True

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    PORT = 4000
    
    with ReuseAddrTCPServer(('0.0.0.0', PORT), ReverseProxyHandler) as httpd:
        print(f'Reverse proxy running on port {PORT}')
        print(f'  - Static files served from: _site/')
        print(f'  - /api/* forwarded to: http://localhost:8080')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nShutting down.')
            httpd.server_close()
