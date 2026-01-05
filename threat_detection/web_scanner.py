import requests
import argparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import time
import sys

class WebAppScanner:
    def __init__(self, target_url, verbose=False):
        self.target_url = target_url.rstrip('/')
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.vulnerabilities = []
        
    def log(self, message, level="INFO"):
        """Log messages"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def crawl_website(self, max_pages=10):
        """Crawl website to discover pages"""
        self.log(f"Crawling {self.target_url}...")
        
        visited = set()
        to_visit = [self.target_url]
        discovered_pages = []
        
        while to_visit and len(visited) < max_pages:
            url = to_visit.pop(0)
            
            if url in visited:
                continue
            
            try:
                response = self.session.get(url, timeout=5)
                visited.add(url)
                discovered_pages.append(url)
                
                if self.verbose:
                    self.log(f"  Found: {url} ({response.status_code})", "DETAIL")
                
                # Extract links
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute_url = urljoin(url, href)
                    
                    # Only follow links within the same domain
                    if self.target_url in absolute_url and absolute_url not in visited:
                        to_visit.append(absolute_url)
                
            except Exception as e:
                if self.verbose:
                    self.log(f"  Error crawling {url}: {e}", "ERROR")
        
        self.log(f"Discovered {len(discovered_pages)} pages")
        return discovered_pages
    
    def check_security_headers(self):
        """Check for security headers"""
        self.log("Checking security headers...")
        
        try:
            response = self.session.get(self.target_url, timeout=5)
            headers = response.headers
            
            security_headers = {
                'X-Frame-Options': 'Missing - Clickjacking vulnerability',
                'X-XSS-Protection': 'Missing - XSS protection',
                'Strict-Transport-Security': 'Missing - HTTPS enforcement',
                'Content-Security-Policy': 'Missing - Content Security Policy',
                'X-Content-Type-Options': 'Missing - MIME sniffing protection'
            }
            
            missing = []
            for header, description in security_headers.items():
                if header not in headers:
                    missing.append(description)
                    self.log(f"  ❌ Missing: {header}", "VULN")
                else:
                    if self.verbose:
                        self.log(f"  ✅ Present: {header}: {headers[header]}", "DETAIL")
            
            if missing:
                self.vulnerabilities.append({
                    'type': 'Missing Security Headers',
                    'risk': 'MEDIUM',
                    'description': '; '.join(missing)
                })
            
        except Exception as e:
            self.log(f"Error checking headers: {e}", "ERROR")
    
    def check_sql_injection(self, url):
        """Check for SQL injection vulnerabilities"""
        self.log(f"Testing {url} for SQL injection...")
        
        # Common SQLi payloads
        payloads = [
            "'",
            "' OR '1'='1",
            "admin' --",
            "1' OR '1'='1",
            "' UNION SELECT NULL--",
            "' AND 1=CONVERT(int, @@version)--"
        ]
        
        # Find forms
        try:
            response = self.session.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            
            for form in forms:
                form_action = form.get('action', '')
                form_url = urljoin(url, form_action) if form_action else url
                form_method = form.get('method', 'get').lower()
                
                # Find input fields
                inputs = form.find_all(['input', 'textarea'])
                input_names = [inp.get('name') for inp in inputs if inp.get('name')]
                
                if input_names:
                    for payload in payloads:
                        # Prepare data
                        data = {}
                        for name in input_names:
                            # Try to identify field types
                            field_type = 'text'
                            for inp in inputs:
                                if inp.get('name') == name:
                                    field_type = inp.get('type', 'text')
                                    break
                            
                            if field_type in ['text', 'email', 'search', 'textarea']:
                                data[name] = payload
                            else:
                                data[name] = 'test'
                        
                        # Submit form
                        try:
                            if form_method == 'post':
                                resp = self.session.post(form_url, data=data, timeout=5)
                            else:
                                resp = self.session.get(form_url, params=data, timeout=5)
                            
                            # Check for SQL error patterns
                            error_patterns = [
                                r'syntax error',
                                r'unclosed quotation',
                                r'SQL Server',
                                r'MySQL',
                                r'ORA-[0-9]',
                                r'PostgreSQL',
                                r'SQLite'
                            ]
                            
                            for pattern in error_patterns:
                                if re.search(pattern, resp.text, re.IGNORECASE):
                                    self.log(f"  ⚠️  Potential SQLi found with payload: {payload}", "VULN")
                                    self.vulnerabilities.append({
                                        'type': 'SQL Injection',
                                        'risk': 'HIGH',
                                        'description': f'Form at {form_url} vulnerable to SQLi',
                                        'payload': payload
                                    })
                                    break
                            
                        except Exception as e:
                            if self.verbose:
                                self.log(f"  Error testing payload {payload}: {e}", "ERROR")
                        
                        time.sleep(0.1)  # Be polite
        
        except Exception as e:
            self.log(f"Error checking SQLi: {e}", "ERROR")
    
    def check_xss(self, url):
        """Check for XSS vulnerabilities"""
        self.log(f"Testing {url} for XSS...")
        
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "\"><script>alert('XSS')</script>",
            "javascript:alert('XSS')"
        ]
        
        try:
            response = self.session.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            
            for form in forms:
                form_action = form.get('action', '')
                form_url = urljoin(url, form_action) if form_action else url
                form_method = form.get('method', 'get').lower()
                
                inputs = form.find_all(['input', 'textarea'])
                input_names = [inp.get('name') for inp in inputs if inp.get('name')]
                
                if input_names:
                    for payload in payloads:
                        data = {}
                        for name in input_names:
                            field_type = 'text'
                            for inp in inputs:
                                if inp.get('name') == name:
                                    field_type = inp.get('type', 'text')
                                    break
                            
                            if field_type in ['text', 'email', 'search', 'textarea']:
                                data[name] = payload
                            else:
                                data[name] = 'test'
                        
                        try:
                            if form_method == 'post':
                                resp = self.session.post(form_url, data=data, timeout=5)
                            else:
                                resp = self.session.get(form_url, params=data, timeout=5)
                            
                            # Check if payload is reflected
                            if payload in resp.text:
                                self.log(f"  ⚠️  Potential XSS found with payload: {payload}", "VULN")
                                self.vulnerabilities.append({
                                    'type': 'Cross-Site Scripting (XSS)',
                                    'risk': 'MEDIUM',
                                    'description': f'Reflected XSS at {form_url}',
                                    'payload': payload
                                })
                                break
                            
                        except Exception as e:
                            if self.verbose:
                                self.log(f"  Error testing XSS payload: {e}", "ERROR")
                        
                        time.sleep(0.1)
        
        except Exception as e:
            self.log(f"Error checking XSS: {e}", "ERROR")
    
    def check_directory_listing(self):
        """Check for directory listing vulnerabilities"""
        self.log("Checking for directory listing...")
        
        common_directories = [
            'admin/', 'backup/', 'config/', 'database/', 'logs/',
            'tmp/', 'uploads/', 'images/', 'css/', 'js/',
            '.git/', '.svn/', '.env', 'phpinfo.php', 'test/'
        ]
        
        for directory in common_directories:
            test_url = f"{self.target_url}/{directory}"
            
            try:
                response = self.session.get(test_url, timeout=3)
                
                # Check for directory listing indicators
                indicators = [
                    'Index of /',
                    'Directory listing for /',
                    '<title>Index of',
                    'Parent Directory</a>'
                ]
                
                for indicator in indicators:
                    if indicator in response.text:
                        self.log(f"  ⚠️  Directory listing enabled: {test_url}", "VULN")
                        self.vulnerabilities.append({
                            'type': 'Directory Listing',
                            'risk': 'LOW',
                            'description': f'Directory listing enabled at {test_url}'
                        })
                        break
                
            except:
                pass  # Directory doesn't exist or timed out
    
    def check_sensitive_files(self):
        """Check for exposed sensitive files"""
        self.log("Checking for sensitive files...")
        
        sensitive_files = [
            'robots.txt', 'sitemap.xml', '.htaccess', '.env',
            'config.php', 'wp-config.php', 'web.config',
            'backup.zip', 'dump.sql', 'error.log'
        ]
        
        for file in sensitive_files:
            test_url = f"{self.target_url}/{file}"
            
            try:
                response = self.session.get(test_url, timeout=3)
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    
                    # Check if it's actually a sensitive file (not error page)
                    if 'html' not in content_type or len(response.text) < 10000:
                        self.log(f"  ⚠️  Sensitive file exposed: {test_url}", "VULN")
                        self.vulnerabilities.append({
                            'type': 'Exposed Sensitive File',
                            'risk': 'MEDIUM',
                            'description': f'Sensitive file exposed at {test_url}'
                        })
                
            except:
                pass
    
    def generate_report(self):
        """Generate web security report"""
        print("\n" + "="*80)
        print("🌐 WEB APPLICATION SECURITY ASSESSMENT REPORT")
        print("="*80)
        print(f"Target: {self.target_url}")
        print(f"Scan Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Vulnerabilities Found: {len(self.vulnerabilities)}")
        print("-"*80)
        
        if self.vulnerabilities:
            # Group by risk level
            by_risk = {'HIGH': [], 'MEDIUM': [], 'LOW': []}
            for vuln in self.vulnerabilities:
                risk = vuln.get('risk', 'MEDIUM')
                by_risk[risk].append(vuln)
            
            for risk_level in ['HIGH', 'MEDIUM', 'LOW']:
                vulns = by_risk[risk_level]
                if vulns:
                    print(f"\n{risk_level} RISK VULNERABILITIES ({len(vulns)}):")
                    for i, vuln in enumerate(vulns, 1):
                        print(f"\n  {i}. {vuln['type']}")
                        print(f"     Description: {vuln['description']}")
                        if 'payload' in vuln:
                            print(f"     Payload: {vuln['payload']}")
        else:
            print("\n✅ No vulnerabilities found!")
        
        print("\n" + "="*80)
        print("🎯 RECOMMENDATIONS:")
        print("  1. Implement all security headers")
        print("  2. Validate and sanitize all user inputs")
        print("  3. Disable directory listing")
        print("  4. Restrict access to sensitive files")
        print("  5. Implement Content Security Policy")
        print("  6. Regular security testing and code review")
        print("="*80)
        
        return self.vulnerabilities

def main():
    parser = argparse.ArgumentParser(description='Web Application Security Scanner')
    parser.add_argument('url', help='Target URL')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-d', '--depth', type=int, default=5, help='Crawl depth')
    
    args = parser.parse_args()
    
    print("="*80)
    print("🔐 WEB APPLICATION SECURITY SCANNER")
    print("="*80)
    print(f"Target: {args.url}")
    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Install required packages if not present
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4"])
        import requests
        from bs4 import BeautifulSoup
    
    scanner = WebAppScanner(args.url, args.verbose)
    
    try:
        # Discover pages
        pages = scanner.crawl_website(args.depth)
        
        # Run security checks
        scanner.check_security_headers()
        scanner.check_directory_listing()
        scanner.check_sensitive_files()
        
        # Test first few pages for vulnerabilities
        for page in pages[:min(5, len(pages))]:
            scanner.check_sql_injection(page)
            scanner.check_xss(page)
        
        # Generate report
        scanner.generate_report()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Scan interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during scan: {e}")

if __name__ == "__main__":
    main()
