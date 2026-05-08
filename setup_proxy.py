import http.server
import socketserver
import urllib.request
import json
from urllib.parse import urlparse, urljoin

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/'):
            # Forward to comments backend
            target_url = 'http://localhost:8080' + self.path
            try:
                with urllib.request.urlopen(target_url) as response:
                    self.send_response(response.status)
                    for header, value in response.headers.items():
                        self.send_header(header, value)
                    self.end_headers()
                    self.wfile.write(response.read())
            except Exception as e:
                self.send_error(500, str(e))
        else:
            # Serve static files
            super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            # Forward to comments backend
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            target_url = 'http://localhost:8080' + self.path
            try:
                req = urllib.request.Request(
                    target_url,
                    data=body,
                    headers=dict(self.headers),
                    method='POST'
                )
                with urllib.request.urlopen(req) as response:
                    self.send_response(response.status)
                    for header, value in response.headers.items():
                        self.send_header(header, value)
                    self.end_headers()
                    self.wfile.write(response.read())
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(405)

if __name__ == '__main__':
    os.chdir('_site')
    with socketserver.TCPServer(('0.0.0.0', 4000), ProxyHandler) as httpd:
        print('Proxy server running on port 4000')
        httpd.serve_forever()
