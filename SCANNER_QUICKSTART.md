# 🚀 Website Security Scanner - Quick Start Guide

## What's New?

Your threat detection system now includes a **Website Security Scanner** that can:

✅ Scan any website for vulnerabilities
✅ Check SSL/TLS certificates
✅ Analyze security headers
✅ Store results in SQLite database
✅ Show threat levels (SAFE, LOW, MEDIUM, HIGH, CRITICAL)
✅ Provide security recommendations
✅ Track scan history

---

## ⚡ Quick Start (5 Minutes)

### **Step 1: Start the Servers**

Open 2 terminals and run:

**Terminal 1 - API Server:**
```powershell
python app/app.py
```

**Terminal 2 - Dashboard Server:**
```powershell
python server.py
```

### **Step 2: Open the Scanner**

1. Go to: http://localhost:8000
2. Click: **🌐 Website Scanner** (in navigation bar)
3. Enter: A website URL (e.g., `https://www.google.com`)
4. Click: **🔍 Scan Website**

### **Step 3: View Results**

You'll see:
- 📊 Threat Level (with color indicator)
- 🎯 Threat Score (0-100)
- 🚨 Vulnerabilities Found (list with details)
- 💡 Security Recommendations (how to stay safe)

---

## 📊 Understanding Threat Levels

### **🟢 SAFE** (Score 0-20)
- No major issues
- **Safe to use normally**
- Can enter passwords and credit cards
- Perfect for online shopping

### **🔵 LOW** (Score 20-50)
- Minor security issues
- **Use with caution**
- Avoid sensitive operations if possible
- Use strong password

### **🟠 MEDIUM** (Score 50-80)
- Notable security concerns
- **Don't enter sensitive data**
- Use separate password
- Enable 2FA if available

### **🔴 HIGH** (Score 80+)
- Serious vulnerabilities
- **Avoid if possible**
- Don't use for shopping
- Don't enter passwords

### **🟣 CRITICAL** (Score 95+)
- Critical security threats
- **DO NOT USE**
- Report to website
- Use alternative

---

## 🔍 What Gets Scanned?

### **1. SSL/TLS Certificate**
✓ Is HTTPS enabled?
✓ Certificate validity
✓ No SSL errors

### **2. Security Headers**
✓ HSTS (Force HTTPS)
✓ CSP (Prevent XSS)
✓ X-Frame-Options (Prevent clickjacking)
✓ X-Content-Type-Options (Prevent MIME sniffing)

### **3. Server Configuration**
✓ Directory listing enabled?
✓ Server version disclosure
✓ Response codes

### **4. Response Analysis**
✓ HTTP status codes
✓ Server information
✓ Technology stack

---

## 💻 Using the Scanner

### **Scan a Website**
```
1. Enter URL in the input box
2. Click "🔍 Scan Website"
3. Wait for results
4. Review threat level and recommendations
```

### **View Scan History**
```
1. Click "📜 Load History" button
2. See all previous scans
3. Click "View" to see full details
4. Review vulnerabilities and recommendations
```

### **Test Common Sites**
```
Safe sites to test:
- https://www.google.com (very secure)
- https://www.github.com (very secure)
- https://www.python.org (secure)

Medium risk sites to test:
- https://www.wikipedia.org (medium security)
```

---

## 🛡️ How to Stay Safe

### **For SAFE Websites (🟢)**
```
✓ Normal browsing is fine
✓ Can shop online
✓ Can enter passwords
✓ Can use payment methods
```

### **For LOW/MEDIUM Websites (🔵🟠)**
```
✓ Use strong, unique password
✓ Enable 2-factor authentication
✓ Don't save password in browser
✓ Use password manager instead
✓ Monitor account activity
```

### **For HIGH Websites (🔴)**
```
⚠ Avoid if possible
⚠ Don't enter personal data
⚠ Use temporary email
⚠ Use VPN
⚠ Monitor for fraud
```

### **For CRITICAL Websites (🟣)**
```
✗ DO NOT USE
✗ Report to authorities
✗ Warn others
✗ Use alternative websites
```

---

## 🔑 Example: How to Use Safely

### **Scenario: Shopping on a Medium-Risk Site**

```
1. Scan the site first: https://www.example-shop.com
2. Results show: MEDIUM (Score: 45/100)
3. You decide: I need to buy something here
4. Precautions:
   ✓ Use strong password (not reused elsewhere)
   ✓ Enable 2-factor authentication
   ✓ Use credit card (not debit) for better protection
   ✓ Check padlock icon in browser
   ✓ Monitor credit card statements weekly
   ✓ Don't save credit card in browser
```

### **Scenario: Before Making a Purchase**

```
1. Find online store: https://newsite.com/shop
2. Scan it first
3. Check results:
   - SAFE (🟢) → Proceed normally
   - LOW (🔵) → Use precautions but OK
   - MEDIUM (🟠) → Only use with careful password
   - HIGH (🔴) → Consider alternatives
   - CRITICAL (🟣) → DO NOT USE
```

---

## 📈 Scanner Statistics

The scanner tracks:
- Total scans performed
- Unique domains scanned
- Average threat score
- Threat level breakdown

View stats with:
```bash
curl http://127.0.0.1:5000/api/scan-statistics
```

---

## 🗄️ Database

Scan results stored in SQLite:
```
Location: ./website_threats.db

Tables:
- website_scans (main results)
- vulnerability_history (detailed vulnerabilities)
```

View with:
```bash
sqlite3 website_threats.db "SELECT * FROM website_scans;"
```

---

## 🔧 API Endpoints

### **Scan a website:**
```bash
curl -X POST http://127.0.0.1:5000/api/scan-website \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.example.com"}'
```

### **Get scan history:**
```bash
curl http://127.0.0.1:5000/api/scan-history
```

### **Get scan details:**
```bash
curl http://127.0.0.1:5000/api/scan/1
```

### **Get statistics:**
```bash
curl http://127.0.0.1:5000/api/scan-statistics
```

### **Scan multiple sites:**
```bash
curl -X POST http://127.0.0.1:5000/api/scan-batch \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://www.site1.com",
      "https://www.site2.com"
    ]
  }'
```

---

## 🧠 Key Concepts

### **Threat Score (0-100)**
- Higher = More vulnerable
- Based on security issues found
- 0-20 = Safe
- 95+ = Critical (don't use)

### **Security Headers**
- Protect against common attacks
- XSS (Cross-Site Scripting)
- Clickjacking
- MIME sniffing
- etc.

### **SSL/TLS Certificate**
- Encrypts data in transit
- Essential for security
- Must be valid and up-to-date

---

## ⚠️ Important Notes

1. **Scanner is Technical:** Checks configuration, not actual exploits
2. **Use Common Sense:** Even SAFE sites can be used badly (weak passwords, phishing links)
3. **Not a Guarantee:** SAFE doesn't mean 100% secure forever
4. **Complementary:** Use with other security practices

---

## 📚 Documentation

For more details, read:
- `WEBSITE_SECURITY_GUIDE.md` - Complete security guide
- `HOW_THREAT_DETECTION_WORKS.md` - How the ML model works
- `MULTI_PAGE_GUIDE.md` - Application overview

---

## 🎯 Next Steps

1. **Test the Scanner:**
   - Scan 5-10 different websites
   - Compare threat levels
   - Review recommendations

2. **Practice Safe Browsing:**
   - Use unique passwords
   - Enable 2FA
   - Monitor accounts

3. **Learn the Vulnerabilities:**
   - Understand what each means
   - Read recommendations
   - Apply to your own sites

---

## 🆘 Troubleshooting

### **Scanner not loading?**
```
✓ Check API server is running: python app/app.py
✓ Check dashboard server: python server.py
✓ Try opening in different browser
```

### **Scans are slow?**
```
✓ Normal - SSL checks can take time
✓ First scan is slower
✓ Network speed affects timing
```

### **Database not saving?**
```
✓ Check write permissions on folder
✓ Check disk space available
✓ Restart servers
```

### **Can't connect to API?**
```
✓ Make sure API server is running
✓ Check port 5000 is not blocked
✓ Check firewall settings
```

---

## 🎉 You're All Set!

Your website security scanner is ready to use! Start scanning websites and stay safe online.

**Remember:** Technology helps, but your judgment is the best security tool. When something feels wrong, it probably is!

🛡️ **Happy Scanning!** 🛡️
