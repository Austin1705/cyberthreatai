#!/usr/bin/env python3
"""
Deploy to Render (Easiest Alternative - No Credit Card Needed)
Automatic deployment in 3 minutes
"""

import json
import os

def create_render_deployment():
    """Create render.yaml for automatic deployment"""
    
    render_config = {
        "services": [
            {
                "name": "threat-detection",
                "type": "web",
                "env": "python",
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "python prod_server.py",
                "envVars": [
                    {
                        "key": "PYTHON_VERSION",
                        "value": "3.10.0"
                    }
                ]
            }
        ]
    }
    
    return render_config

def create_requirements_txt():
    """Create requirements.txt for all dependencies"""
    requirements = """flask==2.3.3
flask-cors==4.0.0
scikit-learn==1.3.1
joblib==1.3.2
requests==2.31.0
numpy==1.24.3
pandas==2.0.3
"""
    return requirements

def main():
    print("\n" + "="*70)
    print("🚀 DEPLOY TO RENDER (FREE, NO CREDIT CARD)")
    print("="*70)
    
    print("\n📋 STEP-BY-STEP GUIDE\n")
    
    print("STEP 1: Create Render Account (1 minute)")
    print("-" * 70)
    print("""
    1. Go to: https://render.com
    2. Click "Sign Up" 
    3. Use GitHub OR email (free account)
    4. Verify email
    
    Done! No credit card needed.
    """)
    
    print("STEP 2: Prepare Your Project (2 minutes)")
    print("-" * 70)
    print("""
    Make sure you have these files in your project:
    
    ✓ prod_server.py
    ✓ app/app.py
    ✓ All .html files
    ✓ All Python modules
    ✓ models/ folder with .joblib files
    
    ✓ requirements.txt (we'll create this)
    """)
    
    print("STEP 3: Create requirements.txt")
    print("-" * 70)
    requirements = create_requirements_txt()
    print("We'll create this file with:")
    print(requirements)
    
    print("\nSTEP 4: Connect GitHub (Optional but Recommended)")
    print("-" * 70)
    print("""
    A. Push your project to GitHub:
       1. Create account: https://github.com
       2. Create new repo: 'threat-detection'
       3. Push your files:
          git init
          git add .
          git commit -m "Initial deployment"
          git branch -M main
          git remote add origin https://github.com/YOUR_USERNAME/threat-detection
          git push -u origin main
    
    B. Or, use Render Web Interface:
       - Upload files directly
       - No GitHub needed
    """)
    
    print("STEP 5: Deploy on Render")
    print("-" * 70)
    print("""
    1. Go to: https://dashboard.render.com
    2. Click "New +" → "Web Service"
    3. Choose:
       - "Build and deploy from GitHub" (if using GitHub)
       - Or "Public Git repository" (paste your repo link)
    4. Configuration:
       Name: threat-detection
       Environment: Python 3.10
       Build Command: pip install -r requirements.txt
       Start Command: python prod_server.py
       
    5. Click "Create Web Service"
    6. Wait 3-5 minutes for deployment
    7. Copy your public URL!
    """)
    
    print("STEP 6: Your Public Website is LIVE! 🎉")
    print("-" * 70)
    print("""
    ✓ URL format: https://threat-detection-xxxx.onrender.com
    
    Access:
    • Dashboard: https://your-url/
    • Reports: https://your-url/reports.html
    • Pentest: https://your-url/pentest.html
    • API: https://your-url/api/health
    
    Share the URL with anyone!
    """)
    
    print("="*70)
    print("⚡ ADVANTAGES OF RENDER")
    print("="*70)
    print("""
    ✅ FREE tier included
    ✅ No credit card required
    ✅ Automatic updates from GitHub
    ✅ Custom domain support
    ✅ 750 free compute hours/month
    ✅ Auto-scaling
    ✅ Green energy powered
    ✅ Simple, clean interface
    """)
    
    print("\n" + "="*70)
    print("📝 CREATING requirements.txt")
    print("="*70 + "\n")
    
    # Create requirements.txt
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("✓ requirements.txt created!")
    print("\nContents:")
    print(requirements)

if __name__ == "__main__":
    main()
