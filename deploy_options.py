#!/usr/bin/env python3
"""
Deploy to Public Web - Using Cloudflare Tunnel (No Auth Required)
"""

import subprocess
import sys
import os
import platform

def main():
    print("\n" + "="*70)
    print("🌐 MAKE YOUR WEBSITE PUBLIC")
    print("="*70)
    
    print("\n📋 OPTION 1: Deploy to Replit (EASIEST - 2 minutes)")
    print("-" * 70)
    print("""
Step 1: Go to https://replit.com and create account
Step 2: Create new Repl > Python
Step 3: Upload all files from your project folder
Step 4: Run this command in Replit terminal:
   pip install flask flask-cors joblib requests
   python prod_server.py

Step 5: Click "Open in new tab" - Your public URL is ready!

Advantage: FREE, PERMANENT, automatic public URL
""")
    
    print("\n📋 OPTION 2: Deploy to Railway (2 minutes)")
    print("-" * 70)
    print("""
Step 1: Go to https://railway.app and create account
Step 2: Create new project > GitHub or import repo
Step 3: Upload your files
Step 4: Set Start Command: python prod_server.py
Step 5: Click deploy - get automatic public URL

Advantage: FREE trial ($5 credit), very fast
""")
    
    print("\n📋 OPTION 3: Deploy to PythonAnywhere (5 minutes)")
    print("-" * 70)
    print("""
Step 1: Go to https://www.pythonanywhere.com/free
Step 2: Create free account
Step 3: Upload your project files
Step 4: Create Web App (Python 3.10)
Step 5: Your URL: https://yourusername.pythonanywhere.com

Advantage: FREE forever, always online
""")
    
    print("\n📋 OPTION 4: Quick Tunnel Using Local Share")
    print("-" * 70)
    print("""
Share your computer's IP for local network access:

From any device on your network, open:
   http://192.168.56.1:8000
   
or

   http://10.220.8.190:8000

Works on same WiFi, but not from outside network.
""")
    
    print("\n" + "="*70)
    print("⭐ RECOMMENDATION")
    print("="*70)
    print("""
BEST: Use Replit (simplest, no configuration needed)
1. Go to https://replit.com
2. Upload your files
3. Click Run
4. Share the public URL

Takes literally 2 minutes!
""")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
