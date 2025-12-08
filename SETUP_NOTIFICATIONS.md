# 📧 Report & Notification System Setup Guide

## Overview

Your threat detection system now includes a powerful **Report & Notification Center** that can:
- 🚨 Send email alerts when websites go down
- 📋 Generate detailed vulnerability reports
- 💾 Store reports locally for offline access
- 📧 Support Gmail, Office 365, and custom email servers

## Quick Setup (2 minutes)

### Step 1: Access the Reports Dashboard
Open your browser and navigate to:
```
http://localhost:8000/reports.html
```

You'll see a professional dashboard with 4 main sections:
- **Send Alert** - Report websites that are down
- **View Reports** - See all saved alerts and reports
- **Email Config** - Set up your email provider
- **Preferences** - Customize notification settings

### Step 2: Configure Gmail (Recommended)

#### Why Gmail?
- Free and reliable
- Works from anywhere
- Easy to set up with App Passwords

#### Setup Steps:

1. **Go to your Google Account:**
   - Open https://myaccount.google.com
   - Select "Security" from left menu

2. **Enable 2-Factor Authentication** (if not already enabled)
   - Click "2-Step Verification"
   - Follow the prompts

3. **Create App Password:**
   - Go back to Security settings
   - Find "App passwords" (appears after 2FA is enabled)
   - Select "Mail" and "Windows"
   - Copy the 16-character password

4. **Enter in Reports Dashboard:**
   - Go to `/reports.html`
   - Click "Email Config" tab
   - Enter:
     ```
     SMTP Server: smtp.gmail.com
     SMTP Port: 587
     Sender Email: your-email@gmail.com
     App Password: (16-character password from step 3)
     Recipient Emails: admin@example.com
     ```
   - Click "Save Configuration"

### Step 3: Send Your First Alert

1. Click "Send Alert" tab
2. Enter a website URL that's actually down (or test with any URL)
3. Add an error message (e.g., "Connection timeout")
4. Click "Send Alert"

You should receive an email within 30 seconds!

---

## Different Email Providers

### Option 1: Gmail (RECOMMENDED) ✅
**Pros:** Free, reliable, easy setup
**Cons:** Requires 2FA

**Configuration:**
```
SMTP Server: smtp.gmail.com
SMTP Port: 587
Sender Email: your-email@gmail.com
Password: App Password (16 chars, not your Gmail password)
```

**Setup:** https://support.google.com/accounts/answer/185833

---

### Option 2: Office 365 / Outlook
**Pros:** If you already use Outlook
**Cons:** Requires office.com subscription

**Configuration:**
```
SMTP Server: smtp.office365.com
SMTP Port: 587
Sender Email: your-email@outlook.com
Password: Your Outlook password
```

---

### Option 3: Corporate Email
**Configuration depends on your IT department:**
```
SMTP Server: (ask IT)
SMTP Port: 25, 465, or 587 (ask IT)
Sender Email: your-email@company.com
Password: Your email password
```

---

## API Integration

### Send Alert via API

```bash
curl -X POST http://localhost:5001/api/report/send-alert \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "error": "Website is not responding",
    "email": "admin@example.com"
  }'
```

### Send Vulnerability Report via API

```bash
curl -X POST http://localhost:5001/api/report/vulnerability \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "vulnerabilities": [
      {
        "type": "SQL Injection",
        "severity": "CRITICAL",
        "description": "User input not sanitized",
        "recommendation": "Use parameterized queries"
      }
    ]
  }'
```

### JavaScript/Fetch Example

```javascript
// Send website down alert
async function sendDownAlert() {
    const response = await fetch('http://127.0.0.1:5001/api/report/send-alert', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            url: 'https://example.com',
            error: 'Connection timeout',
            email: 'admin@example.com'
        })
    });
    
    const result = await response.json();
    console.log('Alert sent:', result);
}

// Send vulnerability report
async function sendVulnReport() {
    const response = await fetch('http://127.0.0.1:5001/api/report/vulnerability', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            url: 'https://example.com',
            vulnerabilities: [
                {
                    type: 'SQL Injection',
                    severity: 'CRITICAL',
                    description: '...',
                    recommendation: '...'
                }
            ]
        })
    });
    
    const result = await response.json();
    console.log('Report sent:', result);
}
```

---

## Automated Alerts from Scanner

The system can automatically send alerts when it detects issues. For example, add this to your website scanner:

```python
# In your scanner code
if scan_result['threat_level'] == 'CRITICAL':
    notifier.send_vulnerability_report(
        url=url,
        vulnerabilities=scan_result['vulnerabilities'],
        severity_counts=scan_result['severity_counts']
    )
```

---

## Testing

### Test from Command Line

Run the included test script:
```powershell
python test_notification_system.py
```

This will:
1. ✓ Check if API is running
2. ✓ Send a test website down alert
3. ✓ Send a test vulnerability report
4. ✓ Retrieve all saved reports
5. ✓ Check local report storage

### Manual Testing in Dashboard

1. Go to `/reports.html`
2. Click "Email Config"
3. Fill in your email settings
4. Click "Test Email" button
5. Check your inbox within 30 seconds

---

## Report Files

All reports are saved locally in the `reports/` directory:

```
reports/
├── alert_example_com_20240812_153022.json
├── vulnerability_example_com_20240812_153100.json
└── ...
```

**View in Dashboard:**
- Go to `/reports.html`
- Click "View Reports" tab
- See all alerts and reports with details

**Download:**
- Click on any report card
- Click "Download" button

---

## Troubleshooting

### "Email not sending" Error

**Check:**
1. Are you using an App Password (not regular password)?
2. Is 2FA enabled on your Gmail?
3. Is your email address spelled correctly?
4. Is your internet connection working?

**Solution:**
1. Re-check your Gmail setup (follow steps above)
2. Test the connection by clicking "Test Email"
3. Check the server console for error messages
4. Try a different email provider (Office 365)

### "SMTP server not found"

**Solution:**
1. Verify SMTP server address (smtp.gmail.com for Gmail)
2. Check your internet connection
3. Ensure port 587 is not blocked by your firewall
4. Try port 25 instead (may be blocked)

### Reports Not Saving

**Solution:**
1. Ensure `reports/` directory exists
2. Check file permissions
3. Check available disk space
4. Try creating a manual report file:
   ```powershell
   mkdir reports
   ```

---

## Integration Examples

### Example 1: Auto-Alert on Website Down

```python
from notification_system import ReportNotificationSystem
import requests

notifier = ReportNotificationSystem()

def check_website_health(url):
    try:
        response = requests.get(url, timeout=5)
        return True
    except:
        # Website is down, send alert
        notifier.send_website_down_alert(
            url=url,
            error_message=f'Website not responding - Connection failed',
            contact_email='admin@example.com'
        )
        return False

# Usage
check_website_health('https://example.com')
```

### Example 2: Report Vulnerabilities from Scanner

```python
from notification_system import ReportNotificationSystem

notifier = ReportNotificationSystem()

vulnerabilities = [
    {
        'type': 'SQL Injection',
        'severity': 'CRITICAL',
        'description': 'Found in /search endpoint',
        'recommendation': 'Use parameterized queries'
    },
    {
        'type': 'Missing HSTS Header',
        'severity': 'HIGH',
        'description': 'HSTS not enabled',
        'recommendation': 'Add Strict-Transport-Security header'
    }
]

notifier.send_vulnerability_report(
    url='https://example.com',
    vulnerabilities=vulnerabilities,
    severity_counts={
        'CRITICAL': 1,
        'HIGH': 1,
        'MEDIUM': 0,
        'LOW': 0
    }
)
```

---

## Features Overview

### 🚨 Website Down Alerts
- Real-time notifications
- Custom error messages
- Email sent within 30 seconds
- Stored locally for audit trail

### 📋 Vulnerability Reports
- Detailed findings with severity levels
- Specific recommendations for each issue
- Color-coded by severity
- Professional email format

### 💾 Local Storage
- All reports saved as JSON files
- Can be reviewed offline
- Useful for compliance/auditing
- No external database needed

### ⚙️ Customizable
- Multiple email providers supported
- Custom notification preferences
- Configurable recipients
- Report filtering and sorting

### 📊 Dashboard
- Beautiful, modern UI
- Real-time report list
- Status indicators
- One-click report download

---

## Security Best Practices

1. **Never share email_config.json** - It contains your App Password
2. **Use App Passwords** - Not your main account password
3. **Enable 2FA** - For Gmail and Office 365
4. **Review recipients** - Only add trusted emails
5. **Rotate passwords** - Change App Password periodically
6. **Secure your server** - Use HTTPS in production
7. **Check .gitignore** - Ensure email_config.json is not in version control

---

## Frequently Asked Questions

**Q: Do I need to provide my real password?**
A: No! For Gmail, use an "App Password" (16 characters). It's safer than your real password.

**Q: Can I send to multiple emails?**
A: Yes! Separate emails with commas: `admin@example.com, security@example.com`

**Q: Where are my reports stored?**
A: In the `reports/` directory as JSON files. You can access them via dashboard or download them.

**Q: Can I send reports automatically?**
A: Yes! Integrate with your scanner or monitoring system using the API endpoints.

**Q: What if I don't have Gmail?**
A: You can use any SMTP server (Office 365, corporate email, etc). Ask your IT for SMTP details.

**Q: Is my password encrypted?**
A: Yes, email_config.json is stored locally. For production, use environment variables instead.

---

## Next Steps

1. ✅ Set up email configuration
2. ✅ Send your first test alert
3. ✅ View reports in dashboard
4. ✅ Integrate with your scanner
5. ✅ Set up monitoring/automation

---

## Support & Docs

- **Dashboard:** http://localhost:8000/reports.html
- **Documentation:** NOTIFICATION_SYSTEM.md
- **Test Script:** python test_notification_system.py
- **API Reference:** See NOTIFICATION_SYSTEM.md

Happy alerting! 🎉
