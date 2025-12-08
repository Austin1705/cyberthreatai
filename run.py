"""
Simple Flask server launcher for threat detection API.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.app import app, init_model

if __name__ == '__main__':
    if init_model():
        print("\n" + "="*50)
        print("  AI Cybersecurity Threat Detection")
        print("="*50)
        print("Running on http://127.0.0.1:5000")
        print("="*50 + "\n")
        app.run(debug=False, host='127.0.0.1', port=5000)
    else:
        print("Failed to load model")
        sys.exit(1)
