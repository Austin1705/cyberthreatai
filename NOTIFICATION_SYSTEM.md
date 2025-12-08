# Report & Notification System

A comprehensive email and notification system for the AI Cybersecurity Threat Detection platform. Get alerts when websites go down or vulnerabilities are discovered.

## Features

✅ **Website Down Alerts** - Instant email when a website stops responding
✅ **Vulnerability Reports** - Detailed reports with severity levels and recommendations
✅ **Local Report Storage** - JSON files saved locally for offline access
✅ **Email Configuration** - Support for Gmail, Office 365, and custom SMTP servers
✅ **Report Dashboard** - Beautiful UI to manage and view all reports
✅ **Notification Preferences** - Customize alert types and frequencies

## Quick Start

### 1. Set Up Email Configuration

1. Navigate to the **Reports & Notification Center** (`/reports.html`)
2. Click on the **Email Config** tab
3. Enter your email details:
   - **SMTP Server**: smtp.gmail.com (for Gmail)
   - **SMTP Port**: 587
   - **Sender Email**: your-email@gmail.com
   - **App Password**: Your Gmail App Password (not your regular password)
   - **Recipients**: admin@example.com (comma-separated for multiple)

### 2. Gmail Setup (Recommended)

For Gmail, you need to:
1. Enable 2-Factor Authentication on your Google Account
2. Create an [App Password](https://myaccount.google.com/apppasswords)
3. Use that App Password in the notification system (not your Gmail password)

### 3. Send Your First Alert

```javascript
// Example: Send website down alert via API
fetch('http://localhost:5001/api/report/send-alert', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        url: 'https://example.com',
        error: 'Connection timeout after 30 seconds',
        email: 'admin@example.com'  // Optional
    })
})
```

## API Endpoints

### Send Website Down Alert
```
POST /api/report/send-alert
```

**Request:**
```json
{
    "url": "https://example.com",
    "error": "Website is not responding",
    "email": "admin@example.com"  // Optional
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Alert sent successfully",
    "report_file": "reports/alert_example_com_20240812_153022.json",
    "url": "https://example.com"
}
```

### Send Vulnerability Report
```
POST /api/report/vulnerability
```

**Request:**
```json
{
    "url": "https://example.com",
    "vulnerabilities": [
        {
            "type": "SQL Injection",
            "severity": "CRITICAL",
            "description": "Unfiltered user input in database query",
            "recommendation": "Use parameterized queries and input validation"
        },
        {
            "type": "Missing Security Headers",
            "severity": "HIGH",
            "description": "X-Frame-Options header not found",
            "recommendation": "Add X-Frame-Options: DENY to all responses"
        }
    ]
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Vulnerability report sent",
    "report_file": "reports/vulnerability_example_com_20240812_153022.json",
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
```
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
            "type": "alert",
            "timestamp": "2024-08-12T15:30:22.123456",
            "data": {
                "type": "website_down_alert",
                "error": "Connection timeout",
                "contacted": "admin"
            }
        }
    ]
}
```

### Download Report
```
GET /api/report/download/<filename>
```

**Response:** File download (JSON format)

## Configuration Files

### email_config.json
The main configuration file for email settings:

```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your-email@gmail.com",
  "sender_password": "your-app-password",
  "recipients": [
    "admin@example.com",
    "security@example.com"
  ]
}
```

**Location:** `c:/Users/Austinsraj/OneDrive/Documents/myproject/email_config.json`

## Python Usage

### Basic Usage
```python
from notification_system import ReportNotificationSystem

# Initialize the notification system
notifier = ReportNotificationSystem()

# Send website down alert
notifier.send_website_down_alert(
    url='https://example.com',
    error_message='Website is not responding - Connection timeout',
    contact_email='admin@example.com'
)

# Send vulnerability report
notifier.send_vulnerability_report(
    url='https://example.com',
    vulnerabilities=[
        {
            'type': 'SQL Injection',
            'severity': 'CRITICAL',
            'description': 'Unfiltered user input',
            'recommendation': 'Use parameterized queries'
        }
    ],
    severity_counts={'CRITICAL': 1, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
)
```

### Save Reports Locally
```python
# Save report to file without sending email
report_file = notifier.save_report_to_file(
    url='https://example.com',
    report_data={
        'vulnerabilities': [...],
        'severity_counts': {...}
    },
    report_type='vulnerability'
)
# Result: reports/vulnerability_example_com_20240812_153022.json
```

### Retrieve All Reports
```python
# Get all saved reports
reports = notifier.get_all_reports()
for report in reports:
    print(f"URL: {report['url']}")
    print(f"Type: {report['type']}")
    print(f"Data: {report['data']}")
```

### Export to PDF
```python
# Export report as PDF (requires reportlab)
pdf_file = notifier.export_report_pdf(
    url='https://example.com',
    report_data={...}
)
```

## Email Alert Templates

### Website Down Alert
```
Subject: 🚨 ALERT: Website Down - https://example.com

Body includes:
- Website URL
- Error message
- Timestamp
- Recommended actions (restart server, check connectivity, etc.)
```

### Vulnerability Report
```
Subject: 🔴 Vulnerability Report - https://example.com

Body includes:
- Website URL
- Severity summary (Critical, High, Medium, Low)
- Detailed vulnerability list with:
  - Type and severity
  - Description
  - Recommendations
```

## Report Storage

All reports are stored locally in the `reports/` directory:

```
reports/
├── alert_example_com_20240812_153022.json
├── vulnerability_example_com_20240812_153100.json
└── vulnerability_example_com_20240812_153145.json
```

**Filename Format:** `{report_type}_{url_slug}_{timestamp}.json`

## Supported Email Providers

### Gmail
- **SMTP Server:** smtp.gmail.com
- **Port:** 587
- **Requires:** App Password (not regular password)
- **2FA:** Required

### Office 365
- **SMTP Server:** smtp.office365.com
- **Port:** 587
- **Requires:** Email password

### Custom SMTP Server
- **SMTP Server:** your-server.com
- **Port:** 25, 465, or 587 (depends on server)
- **Requires:** Email address and password

## Troubleshooting

### Email Not Sending
**Problem:** "Failed to send email: 535 5.7.8 Username and password not accepted"

**Solution:**
- For Gmail: Make sure you're using an App Password, not your regular password
- Ensure 2FA is enabled on your Gmail account
- Check that the email and password are correct

### Connection Timeout
**Problem:** "Connection timeout" or "SMTP server not found"

**Solution:**
- Verify your SMTP server address is correct
- Check your internet connection
- Ensure port 587 is not blocked by your firewall
- For Gmail, try using port 25 or 465 instead

### Reports Not Saving
**Problem:** "Failed to save report: Permission denied"

**Solution:**
- Ensure the `reports/` directory exists and is writable
- Check file permissions on the reports folder
- The directory will be auto-created if missing

## Integration Examples

### Integrate with Website Scanner
```python
@app.route('/api/scan-website', methods=['POST'])
def scan_website():
    # ... existing scan code ...
    
    if result['threat_level'] == 'CRITICAL':
        # Send alert email
        notifier.send_vulnerability_report(
            url=url,
            vulnerabilities=result.get('vulnerabilities', []),
            severity_counts=result.get('severity_counts', {})
        )
    
    return jsonify(result)
```

### Automated Daily Reports
```python
import schedule
from datetime import datetime

def send_daily_report():
    reports = notifier.get_all_reports()
    # Process and summarize reports
    # Send email with summary
    pass

schedule.every().day.at("09:00").do(send_daily_report)
```

## Security Best Practices

1. **Never commit email_config.json** - Add to .gitignore
2. **Use App Passwords** - Don't use your main account password
3. **Enable 2FA** - For Gmail and Office 365
4. **Limit Recipients** - Only add trusted email addresses
5. **Review Reports** - Check saved reports for sensitive information
6. **Rotate Passwords** - Periodically update App Passwords
7. **Secure the Server** - Run on HTTPS in production

## File Structure

```
myproject/
├── notification_system.py          # Main notification module
├── email_config_sample.json         # Sample configuration
├── email_config.json                # Your configuration (git ignored)
├── reports.html                     # Notification dashboard UI
├── app/
│   └── app.py                       # Flask app with report endpoints
└── reports/                         # Saved reports directory
    ├── alert_*.json
    └── vulnerability_*.json
```

## Performance Considerations

- **Email sending** takes 1-5 seconds depending on SMTP server
- **Report files** are stored locally for quick retrieval
- **Large vulnerability lists** (100+ items) may take longer to send
- **Batch reports** should be processed asynchronously in production

## Future Enhancements

- SMS notifications via Twilio
- Slack/Teams integration
- Webhook support for external systems
- Scheduled report generation
- PDF export with charts
- Custom notification templates
- Multi-language support
- Report analytics dashboard

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the logs in the server console
3. Check `reports/` directory for saved reports
4. Verify email configuration in `/reports.html`

## License

© 2024 AI Cybersecurity Threat Detection System
