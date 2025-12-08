"""
Test script for the notification system
Run this to test alerts and reports
"""

import requests
import json
from datetime import datetime

API_URL = 'http://127.0.0.1:5001'

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def test_send_website_down_alert():
    """Test sending a website down alert"""
    print_header("TEST 1: Send Website Down Alert")
    
    payload = {
        'url': 'https://example.com',
        'error': 'Connection timeout after 30 seconds',
        'email': 'admin@example.com'
    }
    
    print(f"Sending alert for: {payload['url']}")
    print(f"Error: {payload['error']}")
    
    try:
        response = requests.post(
            f'{API_URL}/api/report/send-alert',
            json=payload,
            timeout=10
        )
        
        result = response.json()
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if response.ok:
            print("✓ Alert sent successfully!")
        else:
            print("✗ Failed to send alert")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_send_vulnerability_report():
    """Test sending a vulnerability report"""
    print_header("TEST 2: Send Vulnerability Report")
    
    payload = {
        'url': 'https://testapp.com',
        'vulnerabilities': [
            {
                'type': 'SQL Injection',
                'severity': 'CRITICAL',
                'description': 'Unfiltered user input in database query on /search endpoint',
                'recommendation': 'Use parameterized queries and input validation'
            },
            {
                'type': 'Missing Security Headers',
                'severity': 'HIGH',
                'description': 'X-Frame-Options header not found',
                'recommendation': 'Add X-Frame-Options: DENY to all responses'
            },
            {
                'type': 'Weak SSL Configuration',
                'severity': 'MEDIUM',
                'description': 'TLS 1.0 is still enabled',
                'recommendation': 'Disable TLS 1.0 and 1.1, use TLS 1.2 or higher'
            }
        ]
    }
    
    print(f"Sending vulnerability report for: {payload['url']}")
    print(f"Vulnerabilities found: {len(payload['vulnerabilities'])}")
    
    try:
        response = requests.post(
            f'{API_URL}/api/report/vulnerability',
            json=payload,
            timeout=10
        )
        
        result = response.json()
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if response.ok:
            print("\n✓ Vulnerability report sent successfully!")
            print(f"  Total vulnerabilities: {result.get('total_vulnerabilities')}")
            print(f"  Report file: {result.get('report_file')}")
        else:
            print("✗ Failed to send report")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_get_all_reports():
    """Test retrieving all saved reports"""
    print_header("TEST 3: Get All Saved Reports")
    
    try:
        response = requests.get(
            f'{API_URL}/api/report/get-reports',
            timeout=10
        )
        
        result = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Total reports found: {result.get('total')}")
        
        if result.get('reports'):
            print("\nSaved Reports:")
            for i, report in enumerate(result['reports'], 1):
                print(f"\n  {i}. {report['type'].upper()}")
                print(f"     URL: {report['url']}")
                print(f"     Time: {report['timestamp']}")
                print(f"     Data: {json.dumps(report['data'], indent=6)[:200]}...")
        else:
            print("No reports found yet")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_api_health():
    """Test API health status"""
    print_header("TEST 0: Check API Health")
    
    try:
        response = requests.get(
            f'{API_URL}/api/health',
            timeout=5
        )
        
        result = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"API Status: {result.get('status')}")
        
        if response.ok:
            print("✓ API is running and healthy!")
            return True
        else:
            print("✗ API is not responding correctly")
            return False
            
    except Exception as e:
        print(f"✗ Error: Cannot connect to API")
        print(f"  {str(e)}")
        print(f"  Make sure the API server is running on {API_URL}")
        return False

def test_local_storage():
    """Test local report storage"""
    print_header("TEST 4: Check Local Report Storage")
    
    import os
    from pathlib import Path
    
    reports_dir = 'reports'
    
    if os.path.exists(reports_dir):
        files = list(Path(reports_dir).glob('*.json'))
        print(f"Reports directory exists: {reports_dir}/")
        print(f"Files found: {len(files)}")
        
        if files:
            print("\nRecent reports:")
            for file in sorted(files)[-5:]:
                size = os.path.getsize(file)
                print(f"  - {file.name} ({size} bytes)")
    else:
        print(f"Reports directory not found: {reports_dir}/")
        print("It will be created when the first report is saved")

def main():
    """Run all tests"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║  NOTIFICATION SYSTEM TEST SUITE                          ║")
    print("║  " + datetime.now().strftime("%Y-%m-%d %H:%M:%S").center(54) + "  ║")
    print("╚" + "="*58 + "╝")
    
    # Test API health first
    if not test_api_health():
        print("\n⚠ API is not running. Skipping remaining tests.")
        print("Start the API with: python app/app.py")
        return
    
    # Run remaining tests
    test_send_website_down_alert()
    test_send_vulnerability_report()
    test_get_all_reports()
    test_local_storage()
    
    print("\n" + "="*60)
    print("  TESTING COMPLETE")
    print("="*60)
    print("\n📧 View reports at: http://localhost:8000/reports.html")
    print("📖 Documentation: NOTIFICATION_SYSTEM.md\n")

if __name__ == '__main__':
    main()
