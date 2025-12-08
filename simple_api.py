#!/usr/bin/env python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'status': 'home'})

@app.route('/api/test')
def test():
    return jsonify({'status': 'test'})

if __name__ == '__main__':
    print("Starting simple test server...")
    app.run(debug=False, host='0.0.0.0', port=5001)
