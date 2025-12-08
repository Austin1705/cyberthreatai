"""
Flask web application for real-time network threat detection and website security scanning.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
from datetime import datetime
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from website_scanner import WebsiteThreatScanner
from pentest_module import PenetrationTester
from notification_system import ReportNotificationSystem

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

model = None
scaler = None
feature_names = None
website_scanner = None
pentest = None
notifier = ReportNotificationSystem()

def init_model():
    global model, scaler, feature_names
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, 'models', 'threat_detector.joblib')
        scaler_path = os.path.join(base_dir, 'models', 'scaler.joblib')
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        feature_names = ['packet_size', 'packet_rate', 'protocol_tcp', 'protocol_udp',
                        'protocol_icmp', 'src_port_common', 'dst_port_common',
                        'connection_duration', 'payload_entropy', 'retransmission_rate']
        print("[OK] Model loaded successfully")
        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

@app.route('/')
def home():
    return jsonify({'status': 'running', 'service': 'Threat Detection System', 'version': '1.0.0'})

@app.route('/api/health')
def health():
    if model is None:
        return jsonify({'status': 'error'}), 503
    return jsonify({'status': 'ok'})

@app.route('/api/info')
def info():
    return jsonify({'service': 'Threat Detection', 'model': 'Random Forest', 'features': feature_names})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 503
    try:
        data = request.get_json()
        missing = [f for f in feature_names if f not in data]
        if missing:
            return jsonify({'error': 'Missing features', 'missing': missing}), 400
        
        features = [data[f] for f in feature_names]
        features_scaled = scaler.transform([features])
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]
        
        return jsonify({
            'is_malicious': bool(prediction),
            'threat_type': 'Malicious' if prediction else 'Normal',
            'confidence': float(probability[int(prediction)]),
            'malicious_probability': float(probability[1])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/batch-analyze', methods=['POST'])
def batch_analyze():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 503
    try:
        data = request.get_json()
        samples = data.get('samples', [])
        
        results = []
        for sample in samples:
            missing = [f for f in feature_names if f not in sample]
            if missing:
                results.append({'error': 'Missing features'})
                continue
            
            features = [sample[f] for f in feature_names]
            features_scaled = scaler.transform([features])
            prediction = model.predict(features_scaled)[0]
            probability = model.predict_proba(features_scaled)[0]
            
            results.append({
                'is_malicious': bool(prediction),
                'threat_type': 'Malicious' if prediction else 'Normal',
                'confidence': float(probability[int(prediction)])
            })
        
        return jsonify({'total': len(samples), 'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ==================== WEBSITE SCANNING ENDPOINTS ====================

@app.route('/api/scan-website', methods=['POST'])
def scan_website():
    """Scan a website for threats and vulnerabilities."""
    global website_scanner
    
    if website_scanner is None:
        return jsonify({'error': 'Scanner not initialized'}), 503
    
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        print(f"Scanning URL: {url}")
        
        # Perform scan with timeout
        try:
            result = website_scanner.scan_website(url)
        except Exception as scan_error:
            print(f"Scan error: {scan_error}")
            return jsonify({'error': f'Scan failed: {str(scan_error)}'}), 400
        
        print(f"Scan completed, threat level: {result.get('threat_level')}")
        
        # Save to database
        try:
            scan_id = website_scanner.save_scan_result(result)
        except Exception as db_error:
            print(f"Database error: {db_error}")
            return jsonify({'error': f'Failed to save result: {str(db_error)}'}), 500
        
        return jsonify({
            'scan_id': scan_id,
            'url': result['url'],
            'domain': result['domain'],
            'threat_level': result['threat_level'],
            'threat_score': result['threat_score'],
            'vulnerabilities_found': result['vulnerabilities_found'],
            'vulnerabilities': result['vulnerabilities'],
            'recommendations': result['recommendations'],
            'timestamp': result['scan_timestamp']
        })
    
    except Exception as e:
        print(f"General error in scan_website: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/scan-history', methods=['GET'])
def scan_history():
    """Get scan history."""
    global website_scanner
    
    if website_scanner is None:
        return jsonify({'error': 'Scanner not initialized'}), 503
    
    try:
        domain = request.args.get('domain')
        limit = int(request.args.get('limit', 50))
        
        history = website_scanner.get_scan_history(domain, limit)
        
        return jsonify({
            'scans': history,
            'total': len(history)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/scan/<int:scan_id>', methods=['GET'])
def get_scan_details(scan_id):
    """Get detailed scan results."""
    global website_scanner
    
    if website_scanner is None:
        return jsonify({'error': 'Scanner not initialized'}), 503
    
    try:
        details = website_scanner.get_scan_details(scan_id)
        
        if not details:
            return jsonify({'error': 'Scan not found'}), 404
        
        return jsonify(details)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/scan-statistics', methods=['GET'])
def scan_statistics():
    """Get scan statistics."""
    global website_scanner
    
    if website_scanner is None:
        return jsonify({'error': 'Scanner not initialized'}), 503
    
    try:
        stats = website_scanner.get_statistics()
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/scan-batch', methods=['POST'])
def scan_batch():
    """Scan multiple websites."""
    global website_scanner
    
    if website_scanner is None:
        return jsonify({'error': 'Scanner not initialized'}), 503
    
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        
        if not urls:
            return jsonify({'error': 'URLs list is required'}), 400
        
        results = []
        for url in urls:
            try:
                result = website_scanner.scan_website(url)
                scan_id = website_scanner.save_scan_result(result)
                results.append({
                    'scan_id': scan_id,
                    'url': result['url'],
                    'threat_level': result['threat_level'],
                    'threat_score': result['threat_score']
                })
            except Exception as e:
                results.append({
                    'url': url,
                    'error': str(e)
                })
        
        return jsonify({
            'total': len(urls),
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ==================== PENETRATION TESTING ENDPOINTS ====================

@app.route('/api/pentest/full', methods=['POST'])
def full_pentest():
    """Run comprehensive penetration test on target."""
    global pentest
    
    if pentest is None:
        pentest = PenetrationTester()
    
    try:
        data = request.get_json()
        target_url = data.get('target_url')
        
        if not target_url:
            return jsonify({'error': 'Target URL is required'}), 400
        
        print(f"\n[*] Starting full penetration test for: {target_url}")
        results = pentest.run_full_pentest(target_url)
        
        return jsonify({
            'status': 'completed',
            'results': results
        })
    
    except Exception as e:
        print(f"[ERROR] Pentest error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/pentest/port-scan', methods=['POST'])
def port_scan():
    """Scan for open ports."""
    global pentest
    
    if pentest is None:
        pentest = PenetrationTester()
    
    try:
        data = request.get_json()
        target_url = data.get('target_url')
        
        if not target_url:
            return jsonify({'error': 'Target URL is required'}), 400
        
        print(f"[*] Port scanning: {target_url}")
        result = pentest.port_scan(target_url)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/pentest/ssl-tls', methods=['POST'])
def test_ssl():
    """Test SSL/TLS configuration."""
    global pentest
    
    if pentest is None:
        pentest = PenetrationTester()
    
    try:
        data = request.get_json()
        target_url = data.get('target_url')
        
        if not target_url:
            return jsonify({'error': 'Target URL is required'}), 400
        
        print(f"[*] Testing SSL/TLS: {target_url}")
        result = pentest.test_ssl_tls(target_url)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/pentest/http-headers', methods=['POST'])
def test_headers():
    """Check HTTP security headers."""
    global pentest
    
    if pentest is None:
        pentest = PenetrationTester()
    
    try:
        data = request.get_json()
        target_url = data.get('target_url')
        
        if not target_url:
            return jsonify({'error': 'Target URL is required'}), 400
        
        print(f"[*] Testing HTTP headers: {target_url}")
        result = pentest.test_http_headers(target_url)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/pentest/sql-injection', methods=['POST'])
def test_sql():
    """Test for SQL injection vulnerabilities."""
    global pentest
    
    if pentest is None:
        pentest = PenetrationTester()
    
    try:
        data = request.get_json()
        target_url = data.get('target_url')
        
        if not target_url:
            return jsonify({'error': 'Target URL is required'}), 400
        
        print(f"[*] Testing SQL injection: {target_url}")
        result = pentest.test_sql_injection(target_url)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/pentest/xss', methods=['POST'])
def test_xss_vuln():
    """Test for XSS vulnerabilities."""
    global pentest
    
    if pentest is None:
        pentest = PenetrationTester()
    
    try:
        data = request.get_json()
        target_url = data.get('target_url')
        
        if not target_url:
            return jsonify({'error': 'Target URL is required'}), 400
        
        print(f"[*] Testing XSS: {target_url}")
        result = pentest.test_xss(target_url)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/pentest/csrf', methods=['POST'])
def test_csrf_vuln():
    """Test for CSRF vulnerabilities."""
    global pentest
    
    if pentest is None:
        pentest = PenetrationTester()
    
    try:
        data = request.get_json()
        target_url = data.get('target_url')
        
        if not target_url:
            return jsonify({'error': 'Target URL is required'}), 400
        
        print(f"[*] Testing CSRF: {target_url}")
        result = pentest.test_csrf(target_url)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/pentest/authentication', methods=['POST'])
def test_auth():
    """Test authentication mechanisms."""
    global pentest
    
    if pentest is None:
        pentest = PenetrationTester()
    
    try:
        data = request.get_json()
        target_url = data.get('target_url')
        
        if not target_url:
            return jsonify({'error': 'Target URL is required'}), 400
        
        print(f"[*] Testing authentication: {target_url}")
        result = pentest.test_authentication(target_url)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/pentest/directory-enum', methods=['POST'])
def dir_enum():
    """Enumerate directories."""
    global pentest
    
    if pentest is None:
        pentest = PenetrationTester()
    
    try:
        data = request.get_json()
        target_url = data.get('target_url')
        
        if not target_url:
            return jsonify({'error': 'Target URL is required'}), 400
        
        print(f"[*] Enumerating directories: {target_url}")
        result = pentest.enumerate_directories(target_url)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/pentest/dns-enum', methods=['POST'])
def dns_enum():
    """Perform DNS enumeration."""
    global pentest
    
    if pentest is None:
        pentest = PenetrationTester()
    
    try:
        data = request.get_json()
        target_url = data.get('target_url')
        
        if not target_url:
            return jsonify({'error': 'Target URL is required'}), 400
        
        print(f"[*] DNS enumeration: {target_url}")
        result = pentest.dns_enumeration(target_url)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/pentest/subdomain-discovery', methods=['POST'])
def subdomain_disc():
    """Discover subdomains."""
    global pentest
    
    if pentest is None:
        pentest = PenetrationTester()
    
    try:
        data = request.get_json()
        target_url = data.get('target_url')
        
        if not target_url:
            return jsonify({'error': 'Target URL is required'}), 400
        
        print(f"[*] Subdomain discovery: {target_url}")
        result = pentest.subdomain_discovery(target_url)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/report/send-alert', methods=['POST'])
def send_website_alert():
    """Send alert email when website is down."""
    global notifier
    
    try:
        data = request.get_json()
        url = data.get('url')
        error_message = data.get('error', 'Website is not responding')
        contact_email = data.get('email')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Send email alert
        success = notifier.send_website_down_alert(url, error_message, contact_email)
        
        # Save report locally
        report_file = notifier.save_report_to_file(url, {
            'type': 'website_down_alert',
            'error': error_message,
            'contacted': contact_email if contact_email else 'admin'
        }, 'alert')
        
        return jsonify({
            'status': 'success' if success else 'email_failed',
            'message': 'Alert sent successfully' if success else 'Report saved locally, email failed',
            'report_file': report_file,
            'url': url
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/report/vulnerability', methods=['POST'])
def send_vulnerability_report():
    """Send vulnerability report with detailed findings."""
    global notifier
    
    try:
        data = request.get_json()
        url = data.get('url')
        vulnerabilities = data.get('vulnerabilities', [])
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Count vulnerabilities by severity
        severity_counts = {
            'CRITICAL': len([v for v in vulnerabilities if v.get('severity') == 'CRITICAL']),
            'HIGH': len([v for v in vulnerabilities if v.get('severity') == 'HIGH']),
            'MEDIUM': len([v for v in vulnerabilities if v.get('severity') == 'MEDIUM']),
            'LOW': len([v for v in vulnerabilities if v.get('severity') == 'LOW'])
        }
        
        # Send email report
        success = notifier.send_vulnerability_report(url, vulnerabilities, severity_counts)
        
        # Save report locally
        report_file = notifier.save_report_to_file(url, {
            'vulnerabilities': vulnerabilities,
            'severity_counts': severity_counts
        }, 'vulnerability')
        
        return jsonify({
            'status': 'success' if success else 'email_failed',
            'message': 'Vulnerability report sent' if success else 'Report saved locally',
            'report_file': report_file,
            'severity_counts': severity_counts,
            'total_vulnerabilities': len(vulnerabilities)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/report/get-reports', methods=['GET'])
def get_reports():
    """Get all saved reports."""
    global notifier
    
    try:
        reports = notifier.get_all_reports()
        return jsonify({
            'status': 'success',
            'total': len(reports),
            'reports': reports
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/report/download/<filename>', methods=['GET'])
def download_report(filename):
    """Download a specific report file."""
    try:
        from flask import send_file
        import os
        
        filepath = os.path.join('reports', filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'Report not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    if init_model():
        # Initialize website scanner
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, 'website_threats.db')
        website_scanner = WebsiteThreatScanner(db_path)
        
        print("\n" + "="*60)
        print("  AI Cybersecurity Threat Detection & Website Scanner")
        print("="*60)
        print("Network Threat Detection: [OK] Active")
        print("Website Threat Scanner:    [OK] Active")
        print("Report & Notification:     [OK] Active")
        print("Database:                  [OK] " + db_path)
        print("\nRunning on http://127.0.0.1:5001")
        print("="*60 + "\n")
        app.run(debug=False, host='0.0.0.0', port=5001)
    else:
        print("Failed to load model")

