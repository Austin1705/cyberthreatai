"""
Website Threat & Vulnerability Scanner
Scans external websites for security vulnerabilities and threats.
"""

import requests
import sqlite3
import json
import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse
import hashlib
from typing import Dict, List, Tuple

class WebsiteThreatScanner:
    def __init__(self, db_path='website_threats.db'):
        self.db_path = db_path
        self.timeout = 5
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for storing scan results."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Create table for website scans
        c.execute('''
            CREATE TABLE IF NOT EXISTS website_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                domain TEXT NOT NULL,
                scan_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                
                -- Security checks
                ssl_valid BOOLEAN,
                ssl_expiry TEXT,
                http_redirect BOOLEAN,
                headers_secure BOOLEAN,
                
                -- Response analysis
                status_code INTEGER,
                response_time REAL,
                content_length INTEGER,
                
                -- Threat detection
                threat_level TEXT,
                threat_score REAL,
                vulnerabilities_found INTEGER,
                
                -- Details
                vulnerability_details TEXT,
                recommendations TEXT,
                
                -- Additional info
                server_info TEXT,
                last_modified TEXT,
                expires TEXT
            )
        ''')
        
        # Create table for vulnerability history
        c.execute('''
            CREATE TABLE IF NOT EXISTS vulnerability_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER,
                vulnerability_type TEXT,
                severity TEXT,
                description TEXT,
                recommendation TEXT,
                FOREIGN KEY (scan_id) REFERENCES website_scans(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def scan_website(self, url: str) -> Dict:
        """Complete website scan for threats and vulnerabilities."""
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        print(f"\n🔍 Scanning: {url}")
        
        # Parse URL
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        scan_result = {
            'url': url,
            'domain': domain,
            'scan_timestamp': datetime.now().isoformat(),
            'checks': {},
            'vulnerabilities': [],
            'threat_level': 'UNKNOWN',
            'threat_score': 0.0,
            'recommendations': []
        }
        
        # Run all security checks
        self._check_ssl_certificate(url, domain, scan_result)
        self._check_http_headers(url, scan_result)
        self._check_response_analysis(url, scan_result)
        self._check_server_info(url, scan_result)
        self._calculate_threat_level(scan_result)
        
        return scan_result
    
    def _check_ssl_certificate(self, url: str, domain: str, result: Dict):
        """Check SSL certificate validity and security."""
        print("   ✓ Checking SSL certificate...")
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    result['checks']['ssl_valid'] = True
                    result['checks']['ssl_certificate'] = {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                    }
                    
                    # Check expiry
                    import ssl as ssl_module
                    cert_dict = context.get_ca_certs()
                    
        except ssl.SSLError as e:
            result['checks']['ssl_valid'] = False
            result['vulnerabilities'].append({
                'type': 'SSL/TLS',
                'severity': 'HIGH',
                'description': f'SSL Certificate Error: {str(e)}',
                'recommendation': 'Contact website administrator to fix SSL configuration'
            })
            result['threat_score'] += 20
            
        except Exception as e:
            result['checks']['ssl_valid'] = False
            result['vulnerabilities'].append({
                'type': 'SSL/TLS',
                'severity': 'MEDIUM',
                'description': f'Could not verify SSL: {str(e)}',
                'recommendation': 'Verify SSL certificate is properly installed'
            })
            result['threat_score'] += 10
    
    def _check_http_headers(self, url: str, result: Dict):
        """Check for security-related HTTP headers."""
        print("   ✓ Checking HTTP security headers...")
        
        try:
            response = requests.head(url, timeout=self.timeout, allow_redirects=True)
            headers = response.headers
            
            # Critical security headers
            security_headers = {
                'Strict-Transport-Security': 'HSTS (Force HTTPS)',
                'X-Content-Type-Options': 'Prevent MIME sniffing',
                'X-Frame-Options': 'Prevent clickjacking',
                'Content-Security-Policy': 'Prevent XSS attacks',
                'X-XSS-Protection': 'XSS protection',
            }
            
            missing_headers = []
            for header, description in security_headers.items():
                if header not in headers:
                    missing_headers.append(header)
                    result['vulnerabilities'].append({
                        'type': 'Missing Header',
                        'severity': 'MEDIUM',
                        'description': f'Missing {header} ({description})',
                        'recommendation': f'Add {header} to HTTP response headers'
                    })
                    result['threat_score'] += 5
            
            result['checks']['security_headers'] = {
                'present': [h for h in security_headers if h in headers],
                'missing': missing_headers,
                'total_score': (len(security_headers) - len(missing_headers)) / len(security_headers) * 100
            }
            
        except Exception as e:
            result['checks']['security_headers'] = {'error': str(e)}
    
    def _check_response_analysis(self, url: str, result: Dict):
        """Analyze HTTP response for potential issues."""
        print("   ✓ Analyzing HTTP response...")
        
        try:
            response = requests.get(url, timeout=self.timeout, allow_redirects=True)
            
            result['checks']['response'] = {
                'status_code': response.status_code,
                'content_length': len(response.content),
                'response_time': response.elapsed.total_seconds(),
                'charset': response.encoding
            }
            
            # Check for error pages
            if response.status_code >= 400:
                severity = 'HIGH' if response.status_code >= 500 else 'LOW'
                result['vulnerabilities'].append({
                    'type': 'HTTP Error',
                    'severity': severity,
                    'description': f'Server returned {response.status_code}',
                    'recommendation': 'Check server health and availability'
                })
                result['threat_score'] += (10 if severity == 'HIGH' else 2)
            
            # Check for directory listing
            if '<title>Index of' in response.text:
                result['vulnerabilities'].append({
                    'type': 'Directory Listing',
                    'severity': 'HIGH',
                    'description': 'Directory listing is enabled and accessible',
                    'recommendation': 'Disable directory listing on web server'
                })
                result['threat_score'] += 25
            
            # Check for server information disclosure
            server_header = response.headers.get('Server', '')
            if server_header:
                result['vulnerabilities'].append({
                    'type': 'Server Information Disclosure',
                    'severity': 'LOW',
                    'description': f'Server discloses version: {server_header}',
                    'recommendation': 'Remove or obfuscate Server header'
                })
                result['threat_score'] += 3
            
        except Exception as e:
            result['checks']['response'] = {'error': str(e)}
    
    def _check_server_info(self, url: str, result: Dict):
        """Gather server information."""
        print("   ✓ Checking server information...")
        
        try:
            response = requests.get(url, timeout=self.timeout)
            
            result['checks']['server_info'] = {
                'server': response.headers.get('Server', 'Unknown'),
                'powered_by': response.headers.get('X-Powered-By', 'Unknown'),
                'cdn': response.headers.get('X-CDN-Provider', 'None'),
            }
            
        except Exception as e:
            result['checks']['server_info'] = {'error': str(e)}
    
    def _calculate_threat_level(self, result: Dict):
        """Calculate overall threat level based on vulnerabilities."""
        
        # Cap threat score at 100
        result['threat_score'] = min(result['threat_score'], 100)
        
        # Determine threat level
        if result['threat_score'] == 0:
            result['threat_level'] = 'SAFE'
        elif result['threat_score'] < 20:
            result['threat_level'] = 'LOW'
        elif result['threat_score'] < 50:
            result['threat_level'] = 'MEDIUM'
        elif result['threat_score'] < 80:
            result['threat_level'] = 'HIGH'
        else:
            result['threat_level'] = 'CRITICAL'
        
        # Generate recommendations
        result['recommendations'] = self._generate_recommendations(result)
        result['vulnerabilities_found'] = len(result['vulnerabilities'])
    
    def _generate_recommendations(self, result: Dict) -> List[str]:
        """Generate security recommendations based on findings."""
        recommendations = []
        
        if result['threat_score'] == 0:
            recommendations.append("✅ Website appears secure. No major vulnerabilities detected.")
        else:
            recommendations.append("⚠️  Security issues found. Review the vulnerabilities list below.")
        
        # Specific recommendations
        if any(v['type'] == 'SSL/TLS' for v in result['vulnerabilities']):
            recommendations.append("🔒 Enable HTTPS/SSL certificate for encrypted communication")
        
        if any(v['type'] == 'Missing Header' for v in result['vulnerabilities']):
            recommendations.append("🛡️  Add security headers (HSTS, CSP, X-Frame-Options)")
        
        if any(v['type'] == 'Directory Listing' for v in result['vulnerabilities']):
            recommendations.append("📁 Disable directory listing on web server")
        
        if any(v['severity'] == 'CRITICAL' for v in result['vulnerabilities']):
            recommendations.append("🚨 CRITICAL: Address critical vulnerabilities immediately")
        
        recommendations.append("📖 Enable logging and monitoring for security events")
        recommendations.append("🔄 Keep software and dependencies up to date")
        recommendations.append("🧪 Perform regular security audits and penetration testing")
        
        return recommendations
    
    def save_scan_result(self, scan_result: Dict) -> int:
        """Save scan result to database."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO website_scans 
            (url, domain, threat_level, threat_score, vulnerabilities_found, 
             vulnerability_details, recommendations, server_info)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            scan_result['url'],
            scan_result['domain'],
            scan_result['threat_level'],
            scan_result['threat_score'],
            scan_result['vulnerabilities_found'],
            json.dumps(scan_result['vulnerabilities']),
            json.dumps(scan_result['recommendations']),
            json.dumps(scan_result['checks'].get('server_info', {}))
        ))
        
        scan_id = c.lastrowid
        
        # Save vulnerabilities
        for vuln in scan_result['vulnerabilities']:
            c.execute('''
                INSERT INTO vulnerability_history 
                (scan_id, vulnerability_type, severity, description, recommendation)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                scan_id,
                vuln['type'],
                vuln['severity'],
                vuln['description'],
                vuln['recommendation']
            ))
        
        conn.commit()
        conn.close()
        
        return scan_id
    
    def get_scan_history(self, domain: str = None, limit: int = 50) -> List[Dict]:
        """Get scan history from database."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        if domain:
            c.execute('''
                SELECT id, url, domain, scan_timestamp, threat_level, threat_score, 
                       vulnerabilities_found
                FROM website_scans
                WHERE domain LIKE ?
                ORDER BY scan_timestamp DESC
                LIMIT ?
            ''', (f'%{domain}%', limit))
        else:
            c.execute('''
                SELECT id, url, domain, scan_timestamp, threat_level, threat_score, 
                       vulnerabilities_found
                FROM website_scans
                ORDER BY scan_timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        rows = c.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'url': row[1],
                'domain': row[2],
                'timestamp': row[3],
                'threat_level': row[4],
                'threat_score': row[5],
                'vulnerabilities': row[6]
            }
            for row in rows
        ]
    
    def get_scan_details(self, scan_id: int) -> Dict:
        """Get detailed scan results."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('SELECT * FROM website_scans WHERE id = ?', (scan_id,))
        row = c.fetchone()
        
        if not row:
            return None
        
        # Get vulnerabilities
        c.execute('''
            SELECT vulnerability_type, severity, description, recommendation
            FROM vulnerability_history
            WHERE scan_id = ?
        ''', (scan_id,))
        
        vulns = c.fetchall()
        conn.close()
        
        return {
            'id': row['id'],
            'url': row['url'],
            'domain': row['domain'],
            'timestamp': row['scan_timestamp'],
            'threat_level': row['threat_level'],
            'threat_score': row['threat_score'],
            'vulnerabilities_found': row['vulnerabilities_found'],
            'vulnerabilities': [
                {
                    'type': v['vulnerability_type'],
                    'severity': v['severity'],
                    'description': v['description'],
                    'recommendation': v['recommendation']
                }
                for v in vulns
            ],
            'recommendations': json.loads(row['recommendations']) if row['recommendations'] else [],
            'server_info': json.loads(row['server_info']) if row['server_info'] else {}
        }
    
    def get_statistics(self) -> Dict:
        """Get scan statistics."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('SELECT COUNT(*) FROM website_scans')
        total_scans = c.fetchone()[0]
        
        c.execute('SELECT AVG(threat_score) FROM website_scans')
        avg_threat = c.fetchone()[0] or 0
        
        c.execute('''
            SELECT threat_level, COUNT(*) 
            FROM website_scans 
            GROUP BY threat_level
        ''')
        threat_breakdown = dict(c.fetchall())
        
        c.execute('''
            SELECT COUNT(DISTINCT domain) FROM website_scans
        ''')
        unique_domains = c.fetchone()[0]
        
        conn.close()
        
        return {
            'total_scans': total_scans,
            'unique_domains': unique_domains,
            'average_threat_score': round(avg_threat, 2),
            'threat_breakdown': threat_breakdown
        }


def demo_scan():
    """Demo: Scan some websites."""
    scanner = WebsiteThreatScanner()
    
    websites = [
        'https://www.google.com',
        'https://www.github.com',
        'https://www.python.org',
        'https://www.wikipedia.org',
    ]
    
    print("\n" + "="*80)
    print("  WEBSITE THREAT SCANNER DEMO")
    print("="*80)
    
    for website in websites:
        try:
            result = scanner.scan_website(website)
            scan_id = scanner.save_scan_result(result)
            
            print(f"\n{'='*80}")
            print(f"URL: {result['url']}")
            print(f"Threat Level: {result['threat_level']}")
            print(f"Threat Score: {result['threat_score']:.1f}/100")
            print(f"Vulnerabilities Found: {result['vulnerabilities_found']}")
            print(f"\nRecommendations:")
            for rec in result['recommendations']:
                print(f"  {rec}")
            
            if result['vulnerabilities']:
                print(f"\nVulnerabilities:")
                for vuln in result['vulnerabilities']:
                    print(f"  [{vuln['severity']}] {vuln['type']}: {vuln['description']}")
            
        except Exception as e:
            print(f"Error scanning {website}: {e}")
    
    # Show statistics
    stats = scanner.get_statistics()
    print(f"\n{'='*80}")
    print("SCAN STATISTICS")
    print(f"{'='*80}")
    print(f"Total Scans: {stats['total_scans']}")
    print(f"Unique Domains: {stats['unique_domains']}")
    print(f"Average Threat Score: {stats['average_threat_score']}/100")
    print(f"Threat Breakdown: {stats['threat_breakdown']}")


if __name__ == '__main__':
    demo_scan()
