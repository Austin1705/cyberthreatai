"""
Production HTTP server to serve the project dashboard on local network
Run this to access the project from other computers: http://<your-ip>:8000
"""

import http.server
import socketserver
import os
from pathlib import Path
import socket

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

# Get local IP address
def get_local_ip():
    try:
        # Connect to a non-routable address to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

local_ip = get_local_ip()

# Create HTTP server - bind to 0.0.0.0 for network access
with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
    print("\n" + "="*70)
    print("  📊 AI THREAT DETECTION DASHBOARD - PRODUCTION SERVER")
    print("="*70)
    print(f"✓ Local Access:   http://localhost:{PORT}")
    print(f"✓ Network Access: http://{local_ip}:{PORT}")
    print(f"✓ API Server:     http://{local_ip}:5001")
    print("="*70)
    print("Share the Network Access URL with other users on your network")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
