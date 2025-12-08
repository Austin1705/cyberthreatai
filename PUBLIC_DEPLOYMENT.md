# 🌐 Public Website Deployment Guide

## Option 1: INSTANT PUBLIC ACCESS (30 seconds)

### Step 1: Install Tunneling Service
```powershell
pip install pyngrok
```

### Step 2: Start Public Tunnel
```powershell
python deploy_public.py
```

### Step 3: Share the Link
Copy the public URL that appears (looks like: `https://xxxx-xx-xxx-xxx.ngrok-free.app`)

Share with anyone - they can access immediately!

---

## Option 2: Permanent Hosting (Recommended)

### Deploy to Heroku (Free)

1. **Create Account**: https://heroku.com
2. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
3. **Login**:
```powershell
heroku login
```

4. **Create Heroku App**:
```powershell
cd c:\Users\Austinsraj\OneDrive\Documents\myproject
heroku create your-app-name
```

5. **Deploy**:
```powershell
git init
git add .
git commit -m "Initial deployment"
git push heroku main
```

6. **Access**:
```
https://your-app-name.herokuapp.com
```

---

### Deploy to PythonAnywhere (Free)

1. **Create Account**: https://www.pythonanywhere.com
2. **Upload Files**: Drag & drop your project files
3. **Set Web App**:
   - Web app configuration → Add web app
   - Choose Python 3.10+
   - Configure WSGI file
4. **Access**: `https://username.pythonanywhere.com`

---

### Deploy to Railway (Free $5/month credit)

1. **Create Account**: https://railway.app
2. **Connect GitHub** or upload files
3. **Deploy**:
   - Select Python as environment
   - Set start command: `python prod_server.py`
4. **Get Public URL**: Automatically generated

---

### Deploy to Replit (Free)

1. **Create Account**: https://replit.com
2. **Create Repl**: Choose Python
3. **Upload Project Files**
4. **Run**:
```bash
pip install flask flask-cors joblib requests
python app/app.py &
python prod_server.py
```
5. **Public URL**: Generated automatically

---

### Deploy to Cloud (AWS/Google Cloud/Azure)

#### **Google Cloud Run** (Free tier available)
```bash
# Install Google Cloud SDK
# Login
gcloud auth login

# Deploy
gcloud run deploy threat-detection --source . --platform managed --region us-central1 --allow-unauthenticated
```

#### **AWS Lightsail**
- Simple, cheap ($3-5/month)
- Create instance → Upload files → Access

#### **Azure App Service**
- Create Web App → Deploy files → Auto scaling

---

## Option 3: DNS & Custom Domain

### Get Free Domain
1. **Freenom.com**: Free .tk, .ml, .ga domains
2. **Create Domain**: Register your domain
3. **Point to Your Host**: Add DNS records
4. **Benefits**: 
   - Professional look
   - Easier to remember
   - Better for sharing

### Example Domain Setup
- Domain: `mythreatdetector.tk`
- Points to: Your hosting URL
- Access: `https://mythreatdetector.tk`

---

## Quick Comparison

| Method | Speed | Cost | Permanent | Ease |
|--------|-------|------|-----------|------|
| ngrok (pyngrok) | Instant | Free | No (30min) | ⭐⭐⭐⭐⭐ |
| Cloudflare Tunnel | Instant | Free | No (keep running) | ⭐⭐⭐⭐ |
| Heroku | 5min | Free | Yes | ⭐⭐⭐⭐ |
| Railway | 5min | Free trial | Yes | ⭐⭐⭐⭐ |
| PythonAnywhere | 5min | Free | Yes | ⭐⭐⭐ |
| AWS Lightsail | 10min | $3/month | Yes | ⭐⭐⭐ |

---

## RECOMMENDED: Option 1 (ngrok) + Option 2 (Heroku)

**For Now (Instant):**
```powershell
python deploy_public.py
```
- Share the link immediately
- Works for 2 hours (free tier)
- Anyone can access

**For Permanent (Later):**
Follow Heroku steps above for permanent hosting

---

## Security Notes

⚠️ **Public Access Means:**
- Anyone with the link can use your system
- Be careful with sensitive websites to scan
- Consider adding authentication for production
- Monitor usage regularly

### Optional: Add Password Protection
```python
# Add to app/app.py
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    return username == "admin" and password == "your-password"

@app.route('/api/scan-website', methods=['POST'])
@auth.login_required
def scan_website():
    # ... existing code
```

---

## Testing Links

Once deployed, test these:
- `https://your-url/` → Dashboard
- `https://your-url/reports.html` → Report Center
- `https://your-url/api/health` → API Status
- `https://your-url/pentest.html` → Pen Testing

---

## Troubleshooting

### "ngrok not found"
```powershell
pip install pyngrok
python deploy_public.py
```

### "Port 8000 already in use"
```powershell
Stop-Process -Name python -Force
python deploy_public.py
```

### "Tunnel expired"
- Free ngrok tunnel lasts 2 hours
- Upgrade account for longer tunnels
- Use Heroku/Railway for permanent solution

### "Can't access from mobile"
- Ensure mobile is connected to internet
- Try the exact URL provided
- Clear browser cache
- Try different browser

---

## Share Instructions for Others

**Copy & paste this for people accessing your site:**

```
🌐 AI Threat Detection System

📍 Website: [YOUR_PUBLIC_URL]

Features:
✅ Real-time threat detection
✅ Website vulnerability scanning
✅ Penetration testing tools
✅ Detailed security reports
✅ Email notifications

How to Use:
1. Open the link above
2. Click "Scan" to analyze websites
3. View detailed reports
4. Send alerts via email

🔐 Report Center: [YOUR_URL]/reports.html
```

---

## Next Steps

1. **Right Now**: Run `python deploy_public.py` for instant public access
2. **Today**: Share the link with team members
3. **This Week**: Set up permanent hosting (Heroku/Railway)
4. **Optional**: Get custom domain for professional appearance

---

**Questions?** Check the troubleshooting section or review the deployment guide.
