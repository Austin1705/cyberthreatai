# 🚀 Deploy to Render (BEST FREE OPTION)

## Why Render?
✅ **Free** - No credit card needed  
✅ **Easy** - 5 minute setup  
✅ **Automatic** - Auto-deploys from GitHub  
✅ **Professional** - Custom domains supported  
✅ **Always Online** - 750 free hours/month (more than enough)  

---

## Quick Start (5 Minutes)

### Step 1: Create Render Account
1. Go to: **https://render.com**
2. Click **"Sign Up"**
3. Use **Email** or **GitHub**
4. Verify your email

✓ No credit card needed!

---

### Step 2: Prepare Your Project

#### A. Using GitHub (Recommended)

**Create GitHub Repository:**
```powershell
cd c:\Users\Austinsraj\OneDrive\Documents\myproject

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial deployment"

# Rename branch to main
git branch -M main

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/threat-detection

# Push to GitHub
git push -u origin main
```

**Before pushing, create `.gitignore`:**
```
__pycache__/
*.pyc
.env
.venv
*.db
```

#### B. Without GitHub (Upload Manually)

Render lets you upload files directly - no GitHub needed.

---

### Step 3: Deploy on Render

1. **Go to**: https://dashboard.render.com
2. **Click**: "New +" button
3. **Select**: "Web Service"
4. **Connect**:
   - If using GitHub: Select your repo
   - If manual: Enter "https://github.com/YOUR_USERNAME/threat-detection"
5. **Configuration**:
   ```
   Name: threat-detection
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python prod_server.py
   Instance Type: Free
   ```
6. **Click**: "Create Web Service"
7. **Wait**: 3-5 minutes for deployment

---

### Step 4: Get Your Public URL

Once deployed, you'll see:
```
https://threat-detection-xxxxx.onrender.com
```

**That's your public website!** 🎉

---

## Access Your Site

### From Anywhere
```
Dashboard:    https://your-url/
Reports:      https://your-url/reports.html
Pentest:      https://your-url/pentest.html
Analytics:    https://your-url/analytics.html
API Status:   https://your-url/api/health
```

### Share with Others
Just send them the URL:
- Works on mobile ✓
- Works on desktop ✓
- Works worldwide ✓
- No installation needed ✓

---

## File Structure

Your project should have:
```
myproject/
├── prod_server.py          ← Web server (required)
├── app/
│   └── app.py              ← Flask API
├── notification_system.py
├── website_scanner.py
├── pentest_module.py
├── models/
│   ├── threat_detector.joblib
│   └── scaler.joblib
├── *.html                  ← All HTML files
├── requirements.txt        ← Dependencies
└── .gitignore             ← Ignore files
```

---

## requirements.txt

Make sure this file is in your project root:

```
flask==2.3.3
flask-cors==4.0.0
scikit-learn==1.3.1
joblib==1.3.2
requests==2.31.0
numpy==1.24.3
pandas==2.0.3
```

(Already created for you!)

---

## Troubleshooting

### "Build Failed"
Check the build logs in Render dashboard:
1. Go to your service
2. Click "Logs" tab
3. Look for error messages
4. Common fixes:
   - Missing `requirements.txt`
   - Missing dependency in requirements
   - Python version mismatch

### "Service isn't running"
1. Check logs for errors
2. Verify `prod_server.py` exists
3. Check start command is correct
4. Restart service: Dashboard → "Restart"

### "Can't access from mobile"
- Copy exact URL from Render
- Test on desktop first
- Clear browser cache
- Try different browser

### "Files uploaded but not showing"
- Wait for build to complete
- Check deployment logs
- Ensure all files were uploaded
- Try manual upload on Render website

---

## Advanced: Custom Domain

Want `https://mythreatdetector.com` instead?

1. **Buy domain**: GoDaddy, Namecheap, or Freenom
2. **In Render Dashboard**:
   - Go to Service settings
   - Find "Custom Domain"
   - Add your domain
   - Follow DNS instructions
3. **Update DNS**: Point to Render nameservers
4. **Done**: Your domain now works!

---

## Keep Site Running

### Free Tier Details
- ✅ 750 free compute hours per month
- ✅ That's 31 days × 24 hours = enough!
- ✅ Auto-spins down after 15 min inactivity
- ✅ Auto-spins up when accessed

### To Prevent Spin-Down
1. **Upgrade to Paid** ($7/month)
2. **Use UptimeRobot** (free):
   - https://uptimerobot.com
   - Add monitor: `https://your-url/api/health`
   - Pings every 5 minutes = always running

---

## Deploy Updates

### If Using GitHub
1. Make changes locally
2. Commit and push:
   ```powershell
   git add .
   git commit -m "Update notification system"
   git push
   ```
3. Render auto-deploys (2-5 min)

### If Using Manual Upload
1. Upload files via Render dashboard
2. Render auto-rebuilds
3. Website updates automatically

---

## Monitor Your Site

### View Logs
- Dashboard → Logs tab
- See all requests and errors
- Real-time monitoring

### Check Status
- Render dashboard shows status
- Green = working
- Red = error

### Get Notifications
- Email alerts for deployment
- Slack integration available
- GitHub integration for commits

---

## Security Checklist

⚠️ Website is public - be careful!

- ✅ Don't scan production systems
- ✅ Setup email config (see reports.html)
- ✅ Monitor active connections
- ✅ Keep dependencies updated
- ✅ Use HTTPS (Render auto-enables)
- ✅ Consider adding authentication

---

## Comparison with Other Options

| Service | Setup | Cost | Forever Free | Always On |
|---------|-------|------|-------------|-----------|
| **Render** | 5 min | Free | ✓ | ~ (15min spin-down) |
| **Railway** | 5 min | $5 trial | ✗ | ✓ |
| **PythonAnywhere** | 10 min | Free | ✓ | ✓ |
| **Heroku** | 5 min | ✗ (paid now) | ✗ | ✓ |
| **AWS** | 15 min | Complex | ✗ | ✓ |

**Render is the best balance of free + easy!**

---

## Next Steps

1. **Right Now**: Create Render account (1 min)
2. **Then**: Push to GitHub or upload files (2 min)
3. **Then**: Deploy on Render (3 min)
4. **Done**: Share your public URL!

---

## Questions?

Check:
1. Render documentation: https://render.com/docs
2. Deployment logs in dashboard
3. This guide's troubleshooting section
4. Render support: https://support.render.com

---

**Ready to deploy?** 🚀

Your AI Threat Detection System will be live in **~10 minutes!**
