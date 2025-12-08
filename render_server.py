#!/usr/bin/env python3
"""
Render-compatible Web Server
Serves static HTML files and API endpoints
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory, redirect, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

PORT = int(os.environ.get('PORT', 8000))

@app.route('/')
def home():
    return redirect('/landing.html')

@app.route('/<path:filename>')
def serve_static(filename):
    if filename == '' or filename == '/':
        return send_from_directory('.', 'landing.html')
    try:
        return send_from_directory('.', filename)
    except:
        return send_from_directory('.', 'landing.html'), 200

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'service': 'Threat Detection System'})

@app.errorhandler(404)
def not_found(error):
    return send_from_directory('.', 'landing.html'), 200

if __name__ == '__main__':
    print(f"🌐 Server running on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
