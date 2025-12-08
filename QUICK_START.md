# 🌐 QUICK DEPLOYMENT REFERENCE

## Your Options (Pick One)

### 🏆 BEST: Render.com
- ✅ FREE (no credit card)
- ✅ 5 minutes setup
- ✅ Always online (750 hrs/month free)
- ✅ Auto-deploy from GitHub
- **👉 Use this one**

### 🥈 GOOD: Railway
- ✅ FREE trial ($5 credit)
- ✅ 5 minutes setup
- ✅ Always online
- Requires credit card (for free tier verification)

### 🥉 OKAY: PythonAnywhere
- ✅ FREE forever
- ✅ Always online
- ⚠️ 10 minutes setup
- Slower than others

---

## START HERE: Deploy to Render (5 Min)

### STEP 1: Create Account
```
Go to: https://render.com
Sign up with email
Verify email
```

### STEP 2: Push to GitHub (Optional but Recommended)
```powershell
# In project folder:
git init
git add .
git commit -m "Initial deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USER/threat-detection
git push -u origin main
```

### STEP 3: Deploy on Render
1. Go to: https://dashboard.render.com
2. Click: "New +" → "Web Service"
3. Connect GitHub repo
4. Fill in:
   - **Name**: threat-detection
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python prod_server.py`
   - **Instance**: Free
5. Click: "Create Web Service"
6. Wait 3-5 min → Done!

### STEP 4: Your URL
Copy: `https://threat-detection-xxxxx.onrender.com`

Share this with anyone! 🎉

---

## What's Ready to Deploy

✅ `prod_server.py` - Web server  
✅ `app/app.py` - Flask API  
✅ All HTML files  
✅ All Python modules  
✅ `requirements.txt` - Dependencies  
✅ `models/` - ML models  

---

## Files to Review

| File | Purpose |
|------|---------|
| `RENDER_DEPLOYMENT.md` | Full Render guide |
| `PUBLIC_DEPLOYMENT.md` | All deployment options |
| `REPLIT_DEPLOYMENT.md` | Replit guide |
| `requirements.txt` | Python dependencies |

---

## Access Your Site

Once deployed:

```
🏠 Dashboard:    https://your-url/
📧 Reports:     https://your-url/reports.html
🔓 Pentest:     https://your-url/pentest.html
📊 Analytics:   https://your-url/analytics.html
⚠️  Threats:     https://your-url/threats.html
🌐 Scanner:     https://your-url/scanner.html
🔌 API Status:  https://your-url/api/health
```

---

## Costs

| Service | Price | Features |
|---------|-------|----------|
| **Render** | FREE | 750 hrs/mo, auto-deploy, custom domains |
| **Railway** | $5/mo | Always online, 500 RAM |
| **PythonAnywhere** | FREE | Always online, limited features |

---

## Troubleshooting

**"Build failed"** → Check logs in Render, look for missing dependencies

**"Can't access"** → Wait 5 minutes for first deploy, then try again

**"Slow loading"** → Render spins down after 15 min inactivity, takes 30 sec to wake

**"Need it always running"** → Upgrade to paid ($7/mo) or use UptimeRobot to ping

---

## After Deployment

1. **Setup Email** (optional):
   - Visit: `/reports.html`
   - Go to "Email Config"
   - Add Gmail + app password

2. **Share URL**:
   - Copy your Render URL
   - Send to team
   - Works on any device

3. **Monitor**:
   - Check Render dashboard
   - View real-time logs
   - Monitor uptime

---

## Next: Choose Your Option

**→ Use Render** (recommended)
- Simplest
- Completely free
- Best support
- Deploy in 5 minutes

**Or other options** - see `PUBLIC_DEPLOYMENT.md`

---

**Ready?** Start at Step 1 above! 🚀
