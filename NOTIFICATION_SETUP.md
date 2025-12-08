# 📧 Notification System Setup Guide

## Quick Start

### Step 1: Create Email Configuration
Copy `email_config_sample.json` to `email_config.json` and update with your email:

```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your-email@gmail.com",
  "sender_password": "your-app-password",
  "recipients": ["admin@example.com", "security@example.com"]
}
```

### Step 2: Get Gmail App Password
1. Go to https://myaccount.google.com/apppasswords
2. Enable 2-Factor Authentication (if not already)
3. Generate an App Password for "Mail" on "Windows Computer"
4. Copy the 16-character password (remove spaces)
5. Paste into `sender_password` field in `email_config.json`

### Step 3: Access Report Center
- Visit: **http://localhost:8000/reports.html**
- Or click **📧 Report** button on Dashboard

## Features

### Send Website Down Alerts
- **URL**: Website that is not responding
- **Error**: Description of the error
- **Recipient**: Optional email (uses config if empty)
- **Result**: HTML email with clear action items

### Send Vulnerability Reports
- **URL**: Website scanned
- **Vulnerabilities**: JSON array with findings
- **Auto-sends**: Severity summary + full details
- **Saved locally**: All reports saved as JSON files

### View Saved Reports
- Browse all generated reports
- Filter by type (alerts, vulnerabilities)
- Download and review offline
- Organized by timestamp

### Manage Preferences
- Choose alert types (downtime, vulnerabilities, daily summaries)
- Set notification frequency
- Select report formats (Email, JSON, PDF)
- Configure email recipients

## API Endpoints

### Send Alert
```bash
POST /api/report/send-alert
Content-Type: application/json

{
  "url": "https://example.com",
  "error": "Connection timeout - port 443 unreachable",
  "email": "admin@example.com"  # optional
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Alert sent successfully",
  "report_file": "reports/alert_example_com_20250108_150230.json",
  "url": "https://example.com"
}
```

### Send Vulnerability Report
```bash
POST /api/report/vulnerability
Content-Type: application/json

{
  "url": "https://example.com",
  "vulnerabilities": [
    {
      "type": "SQL Injection",
      "severity": "CRITICAL",
      "description": "Input not sanitized in login form",
      "recommendation": "Use prepared statements and input validation"
    },
    {
      "type": "Missing HTTPS",
      "severity": "HIGH",
      "description": "Site accessible over HTTP",
      "recommendation": "Install SSL certificate and force HTTPS redirect"
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Vulnerability report sent",
  "severity_counts": {
    "CRITICAL": 1,
    "HIGH": 1,
    "MEDIUM": 0,
    "LOW": 0
  },
  "total_vulnerabilities": 2
}
```

### Get All Reports
```bash
GET /api/report/get-reports
```

**Response:**
```json
{
  "status": "success",
  "total": 5,
  "reports": [
    {
      "url": "https://example.com",
      "type": "vulnerability",
      "timestamp": "2025-01-08T15:02:30.123456",
      "data": { ... }
    }
  ]
}
```

## Email Templates

### Website Down Alert
- **From**: Configured sender email
- **Subject**: 🚨 ALERT: Website Down - {URL}
- **Content**: 
  - Current status
  - Error details
  - Timestamp
  - Recommended actions
  - Styled HTML with red accent

### Vulnerability Report
- **From**: Configured sender email
- **Subject**: 🔴 Vulnerability Report - {URL}
- **Content**:
  - Severity summary (counts)
  - Detailed findings per vulnerability
  - Type, Severity, Description, Recommendation
  - Color-coded by severity
  - Professional HTML formatting

## Report Storage

Reports are saved locally in `/reports/` directory as JSON files:

```
reports/
├── alert_example_com_20250108_150230.json
├── vulnerability_example_com_20250108_152015.json
└── alert_test_com_20250108_155600.json
```

### Sample Report Structure
```json
{
  "url": "https://example.com",
  "type": "alert",
  "timestamp": "2025-01-08T15:02:30.123456",
  "data": {
    "type": "website_down_alert",
    "error": "Connection timeout",
    "contacted": "admin@example.com"
  }
}
```

## Troubleshooting

### "Failed to send email"
- ✅ Check `email_config.json` exists in project root
- ✅ Verify Gmail app password (not regular password)
- ✅ Ensure 2FA is enabled on Gmail
- ✅ Check sender email is correct
- ✅ Verify recipient emails are valid

### "SMTP Connection Error"
- ✅ Ensure internet connection is active
- ✅ Check firewall allows port 587
- ✅ Verify SMTP server is correct (smtp.gmail.com for Gmail)
- ✅ Try from a different network if issue persists

### "Reports not showing"
- ✅ Refresh the page
- ✅ Check browser console for errors (F12)
- ✅ Ensure API is running on port 5001
- ✅ Check that `/reports/` directory exists and is writable

### "Email not received"
- ✅ Check spam/promotions folder
- ✅ Verify recipient email is correct
- ✅ Check Gmail sent folder to confirm email was sent
- ✅ Check email provider's security settings

## Advanced Usage

### Custom Email Recipients Per Alert
Instead of using config recipients, pass `email` in request:
```json
{
  "url": "https://example.com",
  "error": "Connection error",
  "email": "specific-person@company.com"
}
```

### Batch Alerts
Send multiple alerts programmatically:
```javascript
const alerts = [
  { url: "https://site1.com", error: "Down" },
  { url: "https://site2.com", error: "Slow response" }
];

for (const alert of alerts) {
  fetch('http://localhost:5001/api/report/send-alert', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(alert)
  });
}
```

### Export Reports as PDF
Install reportlab:
```bash
pip install reportlab
```

Then use the `export_report_pdf()` method in notification_system.py

### Monitor Continuously
Create a cron job or task scheduler to check websites and send alerts if down:
```python
import time
from notification_system import ReportNotificationSystem

notifier = ReportNotificationSystem()
urls = ['https://example.com', 'https://example2.com']

while True:
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            print(f"✓ {url} is up")
        except Exception as e:
            notifier.send_website_down_alert(url, str(e))
    
    time.sleep(300)  # Check every 5 minutes
```

## Integration Examples

### With Pen Test Results
```javascript
// After running pentest, send vulnerability report
const pentest_results = /* from pentest API */;
const vulns = pentest_results.vulnerabilities.map(v => ({
  type: v.test_name,
  severity: v.severity,
  description: v.findings,
  recommendation: v.recommendations[0]
}));

fetch('/api/report/vulnerability', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    url: target_url,
    vulnerabilities: vulns
  })
});
```

### With Website Scanner
```javascript
// After scanning website, send report
const scan_result = /* from scanner API */;

if (scan_result.threat_level === 'HIGH' || scan_result.threat_level === 'CRITICAL') {
  fetch('/api/report/vulnerability', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      url: scan_result.url,
      vulnerabilities: scan_result.vulnerabilities
    })
  });
}
```

## Support

For issues or questions:
1. Check this guide's Troubleshooting section
2. Review API error messages in browser console (F12)
3. Check server logs (terminal running app.py)
4. Review saved reports in `/reports/` directory

---

**Version**: 1.0 | **Updated**: December 2025
