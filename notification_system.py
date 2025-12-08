"""
Email and Notification System for Threat Detection Reports
Sends alerts when websites are down or vulnerabilities are found
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import os
from pathlib import Path

class ReportNotificationSystem:
    def __init__(self, email_config=None):
        """Initialize the notification system with email configuration"""
        self.config = email_config or self.load_config()
        self.reports_dir = 'reports'
        Path(self.reports_dir).mkdir(exist_ok=True)
    
    def load_config(self):
        """Load email configuration from file or use defaults"""
        config_file = 'email_config.json'
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        return {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': 'your-email@gmail.com',
            'sender_password': 'your-app-password',
            'recipients': ['admin@example.com']
        }
    
    def send_website_down_alert(self, url, error_message, contact_email=None):
        """Send alert when website is not responding"""
        subject = f"🚨 ALERT: Website Down - {url}"
        
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; border-left: 5px solid #ff4444;">
                    <h2 style="color: #ff4444;">⚠️ Website Down Alert</h2>
                    
                    <p><strong>URL:</strong> <code style="background-color: #f0f0f0; padding: 2px 6px;">{url}</code></p>
                    
                    <p><strong>Status:</strong> <span style="color: #ff4444; font-weight: bold;">NOT RESPONDING</span></p>
                    
                    <p><strong>Error:</strong></p>
                    <pre style="background-color: #f0f0f0; padding: 10px; border-radius: 4px; overflow-x: auto;">{error_message}</pre>
                    
                    <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <h3 style="color: #333;">Recommended Actions:</h3>
                    <ul>
                        <li>Check if the server is running</li>
                        <li>Verify network connectivity</li>
                        <li>Check firewall rules</li>
                        <li>Review server logs for errors</li>
                    </ul>
                    
                    <footer style="margin-top: 20px; padding-top: 10px; border-top: 1px solid #ddd; font-size: 12px; color: #666;">
                        <p>AI Threat Detection System - Automated Alert</p>
                    </footer>
                </div>
            </body>
        </html>
        """
        
        return self.send_email(subject, body, contact_email)
    
    def send_vulnerability_report(self, url, vulnerabilities, severity_counts):
        """Send detailed vulnerability report"""
        subject = f"🔴 Vulnerability Report - {url}"
        
        vuln_html = ""
        for vuln in vulnerabilities:
            severity_color = {
                'CRITICAL': '#8b0000',
                'HIGH': '#ff4444',
                'MEDIUM': '#ffaa00',
                'LOW': '#00aa00'
            }.get(vuln.get('severity', 'LOW'), '#666')
            
            vuln_html += f"""
            <div style="margin: 15px 0; padding: 15px; border-left: 4px solid {severity_color}; background-color: #f9f9f9; border-radius: 4px;">
                <h4 style="margin: 0 0 10px 0; color: {severity_color};">{vuln.get('type', 'Unknown')}</h4>
                <p style="margin: 5px 0;"><strong>Severity:</strong> {vuln.get('severity', 'Unknown')}</p>
                <p style="margin: 5px 0;"><strong>Description:</strong> {vuln.get('description', 'N/A')}</p>
                <p style="margin: 5px 0;"><strong>Recommendation:</strong> {vuln.get('recommendation', 'N/A')}</p>
            </div>
            """
        
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #ff4444;">🔴 Vulnerability Report</h2>
                    
                    <p><strong>URL:</strong> <code style="background-color: #f0f0f0; padding: 2px 6px;">{url}</code></p>
                    
                    <div style="margin: 15px 0; padding: 15px; background-color: #f0f0f0; border-radius: 4px;">
                        <h3 style="margin-top: 0;">Summary</h3>
                        <p>Critical: <strong style="color: #8b0000;">{severity_counts.get('CRITICAL', 0)}</strong></p>
                        <p>High: <strong style="color: #ff4444;">{severity_counts.get('HIGH', 0)}</strong></p>
                        <p>Medium: <strong style="color: #ffaa00;">{severity_counts.get('MEDIUM', 0)}</strong></p>
                        <p>Low: <strong style="color: #00aa00;">{severity_counts.get('LOW', 0)}</strong></p>
                    </div>
                    
                    <h3>Vulnerabilities Found:</h3>
                    {vuln_html}
                    
                    <p><strong>Report Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    
                    <footer style="margin-top: 20px; padding-top: 10px; border-top: 1px solid #ddd; font-size: 12px; color: #666;">
                        <p>AI Threat Detection System - Security Report</p>
                    </footer>
                </div>
            </body>
        </html>
        """
        
        return self.send_email(subject, body)
    
    def send_email(self, subject, body, recipient_email=None):
        """Send email via SMTP"""
        try:
            recipients = [recipient_email] if recipient_email else self.config['recipients']
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config['sender_email']
            msg['To'] = ', '.join(recipients)
            
            # Attach HTML body
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(self.config['sender_email'], self.config['sender_password'])
                server.sendmail(self.config['sender_email'], recipients, msg.as_string())
            
            print(f"✓ Email sent to {', '.join(recipients)}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to send email: {str(e)}")
            return False
    
    def save_report_to_file(self, url, report_data, report_type='scan'):
        """Save report to JSON file for local storage"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.reports_dir}/{report_type}_{url.replace('://', '_').replace('/', '_')}_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump({
                    'url': url,
                    'type': report_type,
                    'timestamp': datetime.now().isoformat(),
                    'data': report_data
                }, f, indent=2)
            
            print(f"✓ Report saved to {filename}")
            return filename
            
        except Exception as e:
            print(f"✗ Failed to save report: {str(e)}")
            return None
    
    def get_all_reports(self):
        """Retrieve all saved reports"""
        reports = []
        for file in Path(self.reports_dir).glob('*.json'):
            try:
                with open(file, 'r') as f:
                    reports.append(json.load(f))
            except:
                pass
        return reports
    
    def export_report_pdf(self, url, report_data):
        """Export report as PDF (requires reportlab library)"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.reports_dir}/report_{url.replace('://', '_').replace('/', '_')}_{timestamp}.pdf"
            
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Add title
            story.append(Paragraph(f"Security Report - {url}", styles['Heading1']))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # Add content
            for key, value in report_data.items():
                story.append(Paragraph(f"<b>{key}:</b> {str(value)}", styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
            
            doc.build(story)
            print(f"✓ PDF report saved to {filename}")
            return filename
            
        except ImportError:
            print("⚠ reportlab not installed. Install with: pip install reportlab")
            return None

# Create sample email configuration file
def create_sample_config():
    """Create a sample email configuration file"""
    config = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "your-email@gmail.com",
        "sender_password": "your-app-password",
        "recipients": [
            "admin@example.com",
            "security@example.com"
        ],
        "notes": "For Gmail: Enable 2FA and create an App Password at https://myaccount.google.com/apppasswords"
    }
    
    with open('email_config_sample.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("Sample config created: email_config_sample.json")

if __name__ == '__main__':
    # Test the system
    create_sample_config()
    
    # Initialize system
    notifier = ReportNotificationSystem()
    
    # Test alert (won't send without proper config)
    print("\n✓ Notification system initialized")
    print("To use email notifications:")
    print("1. Copy email_config_sample.json to email_config.json")
    print("2. Add your Gmail address and app password")
    print("3. Add recipient email addresses")
