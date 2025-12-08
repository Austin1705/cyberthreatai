"""
Simple HTTP server to serve the project dashboard
Run this to access the project at http://localhost:8000
"""

import http.server
import socketserver
import os
from pathlib import Path

# Change to project directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Redirect root to landing.html
        if self.path == '/':
            self.path = '/landing.html'
        return super().do_GET()
    
    def end_headers(self):
        # Add no-cache headers
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

# Create HTTP server
with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("\n" + "="*60)
    print("  📊 PROJECT DASHBOARD SERVER")
    print("="*60)
    print(f"✓ Server running at: http://localhost:{PORT}")
    print(f"✓ Open in browser: http://localhost:{PORT}")
    print("✓ API Server: http://127.0.0.1:5001")
    print("="*60 + "\n")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
