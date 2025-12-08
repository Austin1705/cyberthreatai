# 🚀 Deploy to Replit (2 Minutes)

## ⭐ EASIEST WAY TO GET PUBLIC URL

### Step 1: Create Replit Account
1. Go to **https://replit.com**
2. Click **"Sign up"**
3. Use Google/GitHub or email (takes 30 seconds)

### Step 2: Create New Python Repl
1. Click **"Create"** → **"Repl"**
2. Choose **"Python"**
3. Name it: **threat-detection**
4. Click **"Create Repl"**

### Step 3: Upload Your Files
**Option A: Upload as ZIP**
1. In your project folder, select all files (Ctrl+A)
2. Right-click → **Send to → Compressed (zipped) folder**
3. Upload `myproject.zip` to Replit
4. In Replit, click **"Upload file"** → select ZIP
5. Replit auto-extracts

**Option B: Drag & Drop**
1. On left side of Replit, click **Files** icon
2. Drag your project folders in

### Step 4: Install Dependencies
In Replit terminal (bottom), run:
```bash
pip install flask flask-cors joblib requests
```

### Step 5: Start Your Website
```bash
python prod_server.py
```

### Step 6: Get Your Public URL
Look for this in the output:
```
Server running at: http://xxxx-xxxx-xxxx.replit.dev
```

**That's your PUBLIC URL!** 🎉

---

## 📱 Access From Anywhere
Share your Replit URL with anyone:
- Works on mobile
- Works on any computer
- Works from anywhere in the world
- No setup needed for viewers

### Share Links
```
Dashboard:    https://xxxx-xxxx-xxxx.replit.dev
Reports:     https://xxxx-xxxx-xxxx.replit.dev/reports.html
Pentest:     https://xxxx-xxxx-xxxx.replit.dev/pentest.html
Analytics:   https://xxxx-xxxx-xxxx.replit.dev/analytics.html
```

---

## ⚙️ Troubleshooting

### "Module not found"
```bash
pip install flask flask-cors joblib requests
```

### "Port already in use"
```bash
# Kill existing process
pkill -f python
# Then run again
python prod_server.py
```

### "Can't see output"
- Scroll down in terminal
- Click **"Show all"**
- Refresh page (F5)

### "Can't access from mobile"
- Copy the full URL from Replit
- Test on desktop first
- Try a different browser
- Clear browser cache

---

## 💡 Pro Tips

### Keep It Running 24/7
- **Free Plan**: Replit puts inactive projects to sleep
- **Upgrade ($7/month)**: Always-on hosting
- **Workaround**: Use Replit + UptimeRobot (free uptime monitor)

### Monitor Your Site
1. Go to https://uptimerobot.com
2. Create account
3. Add monitor: `https://your-replit-url/api/health`
4. Get alerts if site goes down

### See Real-Time Logs
- Replit console shows all activity
- See who accesses what
- Track errors in real-time

### Custom Domain (Optional)
- Go to Replit project settings
- Domain section
- Connect your own domain
- Professional look

---

## File Structure for Replit

Your uploaded folder should have:
```
myproject/
├── app/
│   └── app.py          ← Main API
├── prod_server.py      ← Web server
├── notification_system.py
├── website_scanner.py
├── pentest_module.py
├── models/
│   ├── threat_detector.joblib
│   └── scaler.joblib
├── *.html              ← All HTML files
└── ... other files
```

---

## Quick Reference

| Step | Action | Time |
|------|--------|------|
| 1 | Sign up at replit.com | 1 min |
| 2 | Create Python Repl | 30 sec |
| 3 | Upload files | 30 sec |
| 4 | Install packages | 1 min |
| 5 | Run script | 30 sec |
| 6 | Get public URL | Done! |

**Total: ~4 minutes**

---

## After Deployment

### Email Notifications
Remember to setup `email_config.json`:
1. Visit `/reports.html` on your Replit URL
2. Go to "Email Config"
3. Add Gmail address + app password
4. Save

### Share with Team
1. Copy your Replit URL
2. Send to team members
3. They can access from anywhere
4. No installation needed

---

## Security Tips

⚠️ Public website = anyone can access

Recommendations:
- ✅ Change sensitive default values
- ✅ Don't scan production systems
- ✅ Monitor active connections
- ✅ Log all API calls
- ✅ Update email passwords

---

**Ready to deploy?** 🚀

1. Go to https://replit.com
2. Create account
3. Follow steps above
4. Share URL with world

**Your site will be LIVE in 2 minutes!**
