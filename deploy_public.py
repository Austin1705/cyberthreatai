#!/usr/bin/env python3
"""
Public Website Deployment Script
Deploys the threat detection system to be accessible from anywhere
"""

import subprocess
import sys
import time
import os

def install_package(package):
    """Install a Python package"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])

def start_public_deployment():
    """Start ngrok tunnel for public access"""
    try:
        print("\n" + "="*70)
        print("🌐 PUBLIC WEBSITE DEPLOYMENT")
        print("="*70)
        
        # Install pyngrok
        print("\n📦 Installing tunneling service...")
        install_package("pyngrok")
        
        from pyngrok import ngrok
        
        print("✓ Tunneling service ready")
        print("\n⏳ Starting tunnel to port 8000...")
        
        # Create tunnel (free tier)
        public_url = ngrok.connect(8000, "http")
        
        print("\n" + "="*70)
        print("✅ YOUR PUBLIC WEBSITE IS LIVE!")
        print("="*70)
        print(f"\n🌐 PUBLIC URL: {public_url}")
        print(f"\n📱 Share this link with anyone:")
        print(f"   {public_url}")
        print(f"\n📧 Report Center:")
        print(f"   {public_url}/reports.html")
        print(f"\n🔓 Pen Testing:")
        print(f"   {public_url}/pentest.html")
        print(f"\n📊 Analytics:")
        print(f"   {public_url}/analytics.html")
        print(f"\n⚠️  Threats:")
        print(f"   {public_url}/threats.html")
        print(f"\n🌐 Scanner:")
        print(f"   {public_url}/scanner.html")
        
        print("\n" + "="*70)
        print("ℹ️  THIS URL IS PUBLIC - ANYONE WITH THIS LINK CAN ACCESS")
        print("="*70)
        print("\n⏸️  Press Ctrl+C to stop the tunnel")
        print("="*70 + "\n")
        
        # Keep tunnel alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping tunnel...")
            ngrok.kill()
            print("✓ Tunnel stopped")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nAlternative: Use Cloudflare Tunnel (no signup required)")
        print("1. Download cloudflared from https://developers.cloudflare.com/cloudflare-one/connections/connect-applications/install-and-setup/installation/")
        print("2. Run: cloudflared tunnel --url http://localhost:8000")
        sys.exit(1)

if __name__ == "__main__":
    start_public_deployment()
