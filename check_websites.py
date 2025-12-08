"""
External Website Checker
Checks the status and availability of external websites.
"""

import requests
import time
from datetime import datetime
from urllib.parse import urlparse

class WebsiteChecker:
    def __init__(self, timeout=5):
        self.timeout = timeout
        self.results = []
    
    def check_website(self, url, name=None):
        """Check if a website is accessible."""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        display_name = name or urlparse(url).netloc
        
        try:
            start_time = time.time()
            response = requests.head(url, timeout=self.timeout, allow_redirects=True)
            response_time = time.time() - start_time
            
            status = "✓ Online" if response.status_code < 400 else "⚠ Error"
            
            result = {
                'name': display_name,
                'url': url,
                'status_code': response.status_code,
                'status': status,
                'response_time': response_time,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'error': None
            }
            
            self.results.append(result)
            return result
            
        except requests.exceptions.Timeout:
            result = {
                'name': display_name,
                'url': url,
                'status_code': None,
                'status': '✗ Timeout',
                'response_time': None,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'error': 'Request timeout'
            }
            self.results.append(result)
            return result
            
        except requests.exceptions.ConnectionError:
            result = {
                'name': display_name,
                'url': url,
                'status_code': None,
                'status': '✗ Unreachable',
                'response_time': None,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'error': 'Connection refused'
            }
            self.results.append(result)
            return result
            
        except Exception as e:
            result = {
                'name': display_name,
                'url': url,
                'status_code': None,
                'status': '✗ Error',
                'response_time': None,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'error': str(e)
            }
            self.results.append(result)
            return result
    
    def check_multiple(self, websites):
        """Check multiple websites."""
        print("\n" + "="*80)
        print("  EXTERNAL WEBSITE CHECKER")
        print("="*80 + "\n")
        
        for website in websites:
            if isinstance(website, dict):
                result = self.check_website(website['url'], website.get('name'))
            else:
                result = self.check_website(website)
            
            self.print_result(result)
            time.sleep(0.5)  # Avoid rate limiting
        
        self.print_summary()
    
    def print_result(self, result):
        """Print a single result."""
        status = result['status']
        name = result['name']
        
        if result['response_time']:
            timing = f" ({result['response_time']:.2f}s)"
        else:
            timing = ""
        
        print(f"{status} {name}{timing}")
        
        if result['status_code']:
            print(f"   Status Code: {result['status_code']}")
        
        if result['error']:
            print(f"   Error: {result['error']}")
        
        print()
    
    def print_summary(self):
        """Print summary of all checks."""
        online = sum(1 for r in self.results if '✓' in r['status'])
        offline = sum(1 for r in self.results if '✗' in r['status'])
        
        print("="*80)
        print(f"SUMMARY: {online} Online | {offline} Offline | Total: {len(self.results)}")
        print("="*80 + "\n")
        
        return {'online': online, 'offline': offline, 'total': len(self.results)}


def check_popular_sites():
    """Check popular websites."""
    checker = WebsiteChecker(timeout=5)
    
    websites = [
        {'url': 'https://www.google.com', 'name': 'Google'},
        {'url': 'https://www.github.com', 'name': 'GitHub'},
        {'url': 'https://www.stackoverflow.com', 'name': 'Stack Overflow'},
        {'url': 'https://www.python.org', 'name': 'Python.org'},
        {'url': 'https://www.wikipedia.org', 'name': 'Wikipedia'},
        {'url': 'https://www.amazon.com', 'name': 'Amazon'},
        {'url': 'https://www.twitter.com', 'name': 'Twitter/X'},
        {'url': 'https://www.facebook.com', 'name': 'Facebook'},
    ]
    
    checker.check_multiple(websites)
    return checker.results


def check_local_services():
    """Check your local services."""
    checker = WebsiteChecker(timeout=3)
    
    services = [
        {'url': 'http://localhost:8000', 'name': 'Your Dashboard'},
        {'url': 'http://localhost:5000', 'name': 'Your API'},
        {'url': 'http://127.0.0.1:8000', 'name': 'Dashboard (127.0.0.1)'},
        {'url': 'http://127.0.0.1:5000', 'name': 'API (127.0.0.1)'},
    ]
    
    checker.check_multiple(services)
    return checker.results


def check_custom_websites(urls):
    """Check custom websites provided by user."""
    checker = WebsiteChecker(timeout=5)
    checker.check_multiple(urls)
    return checker.results


def interactive_mode():
    """Interactive mode to check custom websites."""
    print("\n" + "="*80)
    print("  INTERACTIVE WEBSITE CHECKER")
    print("="*80)
    print("\nEnter website URLs to check (one per line)")
    print("Type 'done' when finished\n")
    
    urls = []
    while True:
        url = input("Enter URL (or 'done'): ").strip()
        if url.lower() == 'done':
            break
        if url:
            urls.append(url)
    
    if urls:
        checker = WebsiteChecker(timeout=5)
        checker.check_multiple(urls)
        return checker.results
    else:
        print("No URLs entered.")
        return []


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'popular':
            print("\nChecking popular websites...")
            check_popular_sites()
        
        elif sys.argv[1] == 'local':
            print("\nChecking local services...")
            check_local_services()
        
        elif sys.argv[1] == 'custom':
            if len(sys.argv) > 2:
                check_custom_websites(sys.argv[2:])
            else:
                print("Usage: python check_websites.py custom <url1> <url2> ...")
        
        elif sys.argv[1] == 'interactive':
            interactive_mode()
        
        else:
            print(f"Unknown command: {sys.argv[1]}")
            print("\nUsage:")
            print("  python check_websites.py popular     - Check popular websites")
            print("  python check_websites.py local       - Check your local services")
            print("  python check_websites.py custom <url1> <url2> ... - Check custom URLs")
            print("  python check_websites.py interactive - Interactive mode")
    
    else:
        # Default: check local services
        print("\nDefault: Checking local services...")
        check_local_services()
