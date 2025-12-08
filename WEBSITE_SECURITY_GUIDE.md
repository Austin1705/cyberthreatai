# 🌐 Website Security Scanner & Safe Usage Guide

## Overview

Your application now includes a **Website Threat Scanner** that:
- ✅ Scans external websites for security vulnerabilities
- ✅ Stores scan results in a database
- ✅ Shows threat levels and vulnerability scores
- ✅ Provides recommendations for safe usage

---

## 🚀 How to Use the Website Scanner

### **Step 1: Start the Application**

```powershell
# Terminal 1: Start the API server
python app/app.py

# Terminal 2: Start the dashboard
python server.py

# Then open: http://localhost:8000
```

### **Step 2: Go to Website Scanner**

1. Open http://localhost:8000
2. Click **"🌐 Website Scanner"** in the navigation bar
3. Enter a website URL (e.g., `https://www.google.com`)
4. Click **"🔍 Scan Website"**

### **Step 3: Review Results**

The scanner will show:
- 📊 **Threat Level** (SAFE, LOW, MEDIUM, HIGH, CRITICAL)
- 🎯 **Threat Score** (0-100)
- 🚨 **Vulnerabilities Found** (list with details)
- 💡 **Recommendations** (how to stay safe)

---

## 🔍 What Gets Scanned

The website scanner checks for:

### **1. SSL/TLS Certificate**
- ✓ Is the website using HTTPS?
- ✓ Is the certificate valid?
- ✓ Any SSL/TLS errors?

### **2. Security Headers**
Missing headers add vulnerability points:
- `Strict-Transport-Security` (Force HTTPS)
- `X-Content-Type-Options` (Prevent MIME sniffing)
- `X-Frame-Options` (Prevent clickjacking)
- `Content-Security-Policy` (Prevent XSS)
- `X-XSS-Protection` (XSS protection)

### **3. HTTP Response Analysis**
- Server status codes (200, 404, 500, etc.)
- Directory listing enabled? (Security risk!)
- Server information disclosure

### **4. Server Information**
- Server type and version
- Technology stack
- CDN provider

---

## 📊 Threat Levels Explained

### **🟢 SAFE (Score: 0-20)**
```
No major security issues found
✓ Properly configured SSL/TLS
✓ Most security headers present
✓ No critical vulnerabilities
```
**Safe to use!** Normal browsing is fine.

---

### **🔵 LOW (Score: 20-50)**
```
Minor security issues
⚠ Some missing security headers
⚠ Minor configuration issues
```
**Mostly safe** but be cautious with sensitive data (passwords, credit cards).

---

### **🟠 MEDIUM (Score: 50-80)**
```
Notable security concerns
✗ Multiple missing security headers
✗ Server information disclosure
✗ Older technology stack
```
**Use with caution:**
- Don't enter passwords
- Don't send credit card info
- Use separate password manager
- Enable 2FA if available

---

### **🔴 HIGH (Score: 80+)**
```
Serious security vulnerabilities
✗ SSL/TLS issues
✗ Directory listing enabled
✗ Multiple critical issues
```
**Avoid if possible:**
- Don't visit if not necessary
- Don't enter ANY personal data
- Block cookies and tracking
- Use VPN if you must visit

---

### **🟣 CRITICAL (Score: 95+)**
```
Critical security threats
✗ Major SSL/TLS failures
✗ Server completely misconfigured
```
**DO NOT USE:**
- Don't visit at all if possible
- Warn others about the site
- Report to web security teams
- Use alternative websites

---

## 🛡️ How to Stay Safe While Browsing

### **Based on Scan Results:**

#### **If Website is SAFE (🟢)**
```
✓ Normal browsing is safe
✓ Can enter passwords
✓ Can shop online
✓ Can submit forms
```

#### **If Website is LOW/MEDIUM (🔵🟠)**
```
⚠ Use these precautions:
  1. Use strong, unique password
  2. Enable 2-factor authentication (2FA)
  3. Don't save password in browser
  4. Use password manager instead
  5. Check for green padlock (HTTPS)
  6. Verify domain name spelling
  7. Don't share credit cards
  8. Monitor account activity
```

#### **If Website is HIGH/CRITICAL (🔴🟣)**
```
✗ Avoid if possible, but if you must visit:
  1. Use a temporary/burner email
  2. Use VPN to mask IP
  3. Disable JavaScript in browser
  4. Block all cookies and tracking
  5. Use private/incognito mode
  6. Don't save any credentials
  7. Scan results with antivirus after
  8. Monitor for suspicious activity
```

---

## 📋 Common Vulnerabilities & Fixes

### **1. Missing SSL/TLS Certificate**
```
❌ Problem: No HTTPS (not secure)
✓ Solution: Don't enter personal data
💡 Tip: Look for padlock icon in URL bar
```

### **2. Missing Security Headers**
```
❌ Problem: Vulnerable to XSS, clickjacking
✓ Solution: Use browser extensions for security
💡 Tip: Use uBlock Origin, Privacy Badger
```

### **3. Directory Listing Enabled**
```
❌ Problem: Can browse server files
✓ Solution: Report to website administrator
💡 Contact: search site.com/security.txt
```

### **4. Server Information Disclosure**
```
❌ Problem: Reveals software versions (exploitable)
✓ Solution: Don't worry (harder to exploit)
💡 Tip: Hackers will find this anyway
```

---

## 🔐 Safe Browsing Best Practices

### **1. Browser Security**
```
✓ Keep browser updated
✓ Use HTTPS Everywhere extension
✓ Enable auto-update
✓ Clear cookies regularly
✓ Use private mode for sensitive sites
✓ Disable plugins you don't use
```

### **2. Password Security**
```
✓ Use password manager (Bitwarden, 1Password)
✓ Create unique password for each site
✓ Never reuse passwords
✓ Use 12+ characters
✓ Mix: UPPERCASE, lowercase, 123, !@#
✓ Enable 2-factor authentication (2FA)
```

### **3. Personal Data Protection**
```
✓ Minimize personal information shared
✓ Use nicknames instead of real names
✓ Use temp emails for signups
✓ Check privacy policy before entering data
✓ Don't share location data
✓ Disable auto-complete on sensitive forms
```

### **4. Payment Security**
```
✓ Only shop on verified HTTPS sites
✓ Use credit card (easier to dispute) vs debit
✓ Check for padlock icon
✓ Look for security seals (VeriSign, Norton)
✓ Use virtual card numbers when possible
✓ Monitor bank/credit statements
✓ Enable payment notifications
```

### **5. Phishing Prevention**
```
✓ Check sender email address carefully
✓ Don't click links in emails (type URL instead)
✓ Verify domain name spelling
✓ Hover over links to see destination
✓ Never enter password from email link
✓ Look for "official" vs imposter domains
✓ Be suspicious of urgency ("Act now!")
```

---

## 📖 How to Read Scan Results

### **Example Safe Website:**
```
URL: https://www.google.com
Threat Level: SAFE 🟢
Threat Score: 5/100
Vulnerabilities: 0

✓ Valid SSL certificate
✓ All security headers present
✓ No server info disclosure
✓ Modern technology stack

RECOMMENDATIONS:
✓ Website appears secure
🔒 HTTPS is properly configured
🛡️ Security headers are in place
📖 Enable logging and monitoring
```

**What to do:** Normal browsing is completely safe! 👍

---

### **Example Medium-Risk Website:**
```
URL: https://www.oldsite.com
Threat Level: MEDIUM 🟠
Threat Score: 45/100
Vulnerabilities: 3

⚠ Missing 2 security headers
⚠ Server reveals version info
⚠ Older technology stack

RECOMMENDATIONS:
⚠️ Security issues found
🔒 Enable HTTPS/SSL
🛡️ Add security headers
🔄 Keep software updated
```

**What to do:** Avoid sensitive operations. Use precautions if shopping. ⚠️

---

### **Example High-Risk Website:**
```
URL: https://www.badsite.com
Threat Level: HIGH 🔴
Threat Score: 82/100
Vulnerabilities: 6

✗ Directory listing enabled
✗ Multiple missing headers
✗ SSL certificate issues
✗ Very old technology

RECOMMENDATIONS:
🚨 CRITICAL: Address vulnerabilities
🛡️ Fix SSL configuration
📁 Disable directory listing
🔄 Update all software
```

**What to do:** AVOID THIS SITE unless absolutely necessary! 🚫

---

## 🚀 Using the Scanner API

### **Scan a Single Website:**
```bash
curl -X POST http://127.0.0.1:5000/api/scan-website \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.example.com"}'
```

### **Get Scan History:**
```bash
curl http://127.0.0.1:5000/api/scan-history
```

### **Get Scan Details:**
```bash
curl http://127.0.0.1:5000/api/scan/1
```

### **Get Scan Statistics:**
```bash
curl http://127.0.0.1:5000/api/scan-statistics
```

### **Scan Multiple Websites:**
```bash
curl -X POST http://127.0.0.1:5000/api/scan-batch \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://www.site1.com",
      "https://www.site2.com",
      "https://www.site3.com"
    ]
  }'
```

---

## 📊 Database Storage

### **What Gets Stored:**
```
✓ URL scanned
✓ Domain name
✓ Scan timestamp
✓ SSL validity
✓ HTTP status codes
✓ Response times
✓ Threat level
✓ Threat score
✓ Vulnerabilities found
✓ Vulnerability details
✓ Security recommendations
✓ Server information
```

### **Database Locations:**
```
SQLite: ./website_threats.db
Tables:
  - website_scans (main results)
  - vulnerability_history (detailed vulnerabilities)
```

### **View Database:**
```bash
# Install sqlite3 if needed
pip install sqlite3

# List all scans
sqlite3 website_threats.db "SELECT * FROM website_scans;"

# Get vulnerabilities
sqlite3 website_threats.db "SELECT * FROM vulnerability_history;"
```

---

## 🎓 Quick Reference Card

### **Threat Score Guide:**
| Score | Level | Action |
|-------|-------|--------|
| 0-20  | SAFE  | ✅ Use normally |
| 20-50 | LOW   | ⚠️ Use with care |
| 50-80 | MEDIUM | ⚠️ Avoid sensitive data |
| 80+   | HIGH  | ❌ Avoid if possible |
| 95+   | CRITICAL | 🚫 DO NOT USE |

---

### **Security Headers:**
| Header | Purpose | Why Important |
|--------|---------|--------------|
| HSTS | Force HTTPS | Prevent downgrade attacks |
| CSP | Content Security Policy | Prevent XSS attacks |
| X-Frame-Options | Prevent framing | Stop clickjacking |
| X-Content-Type-Options | Prevent MIME sniffing | Stop malware downloads |
| X-XSS-Protection | XSS filter | Extra XSS protection |

---

### **Safe Passwords:**
| Requirement | Example | Why |
|-------------|---------|-----|
| Length | 12+ chars | Harder to crack |
| Mix cases | PaSsWoRd | Increases combinations |
| Numbers | Pass123 | Increases combinations |
| Symbols | P@ss123! | Increases combinations |
| Unique | Different per site | Limits breach damage |
| Manager | Bitwarden | Easy to use |

---

## 🤔 FAQ

**Q: Is the scanner always accurate?**
```
A: The scanner checks technical security headers and configuration.
   It may not detect:
   - Zero-day vulnerabilities
   - Business logic flaws
   - Application-level attacks
   - Social engineering
   
   Use in combination with common sense!
```

**Q: Can I trust websites with "SAFE" rating?**
```
A: SAFE means good technical security. Always:
   - Verify the domain (look for typos)
   - Check for padlock icon
   - Never click suspicious links
   - Use strong passwords
```

**Q: What if a site is HIGH risk but I need to use it?**
```
A: Use these precautions:
   - Enable VPN
   - Use incognito/private mode
   - Use temporary email
   - Don't save credentials
   - Monitor accounts for fraud
```

**Q: How often should I scan websites?**
```
A: Scan when:
   - First time visiting a site
   - Haven't visited in 6+ months
   - Before making purchases
   - Before entering sensitive data
```

---

## 🔐 Emergency Response

### **If You Think You're Compromised:**

1. **Change Passwords Immediately**
   - Use secure computer
   - Generate new strong passwords
   - Change email password first
   - Change banking passwords
   - Use password manager

2. **Monitor Accounts**
   - Check bank statements
   - Review credit reports (annualcreditreport.com)
   - Set fraud alerts
   - Enable 2FA everywhere

3. **Notify Authorities**
   - Report to FTC (identitytheft.gov)
   - Contact your bank
   - File police report if needed

4. **Document Everything**
   - Save emails
   - Take screenshots
   - Keep timeline of events
   - Document financial losses

---

## 🎯 Next Steps

1. **Test the Scanner:**
   - Scan trusted websites (Google, GitHub)
   - Scan lesser-known sites
   - Review the threat scores
   - Check the database

2. **Learn the Vulnerabilities:**
   - Understand what each vulnerability means
   - Read recommendations
   - Apply security headers to your sites

3. **Practice Safe Browsing:**
   - Use unique strong passwords
   - Enable 2FA on all accounts
   - Monitor your accounts
   - Stay updated on security news

---

**Your Website Security Scanner is now active and ready to protect you! 🛡️**

Remember: Technology helps, but **your judgment is the best security tool**. When something feels wrong, it probably is!
