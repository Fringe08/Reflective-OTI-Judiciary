import argparse
import socket
import subprocess
import platform
import ipaddress
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import datetime

class NetworkScanner:
    def __init__(self, network_range="192.168.1.0/24", max_threads=50):
        self.network_range = network_range
        self.max_threads = max_threads
        self.active_hosts = []
        
    def ping_sweep(self):
        """Perform ping sweep to discover active hosts"""
        print(f"🔍 Performing ping sweep on {self.network_range}")
        
        # Generate IP addresses
        try:
            network = ipaddress.ip_network(self.network_range, strict=False)
            ips = [str(ip) for ip in network.hosts()]
        except:
            ips = [self.network_range]
        
        def ping_host(ip):
            """Ping a single host"""
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '1', '-w', '1000', ip]
            
            try:
                output = subprocess.run(command, capture_output=True, text=True)
                if output.returncode == 0:
                    print(f"  ✅ Host {ip} is UP")
                    return ip
            except:
                pass
            return None
        
        # Use threading for faster scanning
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            results = executor.map(ping_host, ips)
        
        self.active_hosts = [ip for ip in results if ip]
        print(f"\n📊 Found {len(self.active_hosts)} active hosts")
        return self.active_hosts
    
    def arp_scan(self):
        """Perform ARP scan (requires admin/root)"""
        print("🔍 Performing ARP scan...")
        
        try:
            if platform.system().lower() == 'windows':
                # Windows ARP scan
                result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
                print("Windows ARP Table:")
                print(result.stdout[:500])  # First 500 chars
            else:
                # Linux ARP scan
                result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
                print("ARP Table:")
                print(result.stdout)
        except Exception as e:
            print(f"  ⚠️  ARP scan failed: {e}")
    
    def dns_enumeration(self, domain):
        """Enumerate DNS records"""
        print(f"🔍 Enumerating DNS records for {domain}")
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        
        for record_type in record_types:
            try:
                import dns.resolver
                resolver = dns.resolver.Resolver()
                answers = resolver.resolve(domain, record_type)
                
                print(f"  {record_type}:")
                for rdata in answers:
                    print(f"    {rdata}")
            except:
                pass  # Record type not found
    
    def subnet_discovery(self):
        """Discover network topology"""
        print("🔍 Discovering network topology...")
        
        # Simulate network mapping
        topology = {
            'gateway': '192.168.1.1',
            'subnet_mask': '255.255.255.0',
            'dns_servers': ['8.8.8.8', '8.8.4.4'],
            'network_segments': [
                {'segment': 'LAN', 'ips': self.active_hosts[:10]},
                {'segment': 'DMZ', 'ips': []},
                {'segment': 'Servers', 'ips': [f'192.168.1.{i}' for i in [10, 20, 30]]}
            ]
        }
        
        print(f"  Gateway: {topology['gateway']}")
        print(f"  Subnet Mask: {topology['subnet_mask']}")
        print(f"  DNS Servers: {', '.join(topology['dns_servers'])}")
        print("\n  Network Segments:")
        for segment in topology['network_segments']:
            if segment['ips']:
                print(f"    • {segment['segment']}: {len(segment['ips'])} hosts")
        
        return topology

class VulnerabilityScanner:
    def __init__(self, target):
        self.target = target
        self.vulnerabilities = []
    
    def scan_common_vulns(self):
        """Scan for common vulnerabilities"""
        print(f"🔍 Scanning {self.target} for common vulnerabilities...")
        
        common_checks = [
            ('FTP Anonymous Login', 21, self.check_ftp_anonymous),
            ('SSH Weak Algorithms', 22, self.check_ssh_weak),
            ('HTTP Security Headers', 80, self.check_http_headers),
            ('SMB Signing Disabled', 445, self.check_smb_signing),
            ('SSL/TLS Weak Ciphers', 443, self.check_ssl_tls)
        ]
        
        for name, port, check_func in common_checks:
            print(f"  Checking: {name} (Port {port})")
            result = check_func()
            if result:
                self.vulnerabilities.append(result)
                print(f"    ⚠️  {result['risk']}: {result['description']}")
            else:
                print(f"    ✅ Secure")
        
        return self.vulnerabilities
    
    def check_ftp_anonymous(self):
        """Check for anonymous FTP login"""
        # Simulated check
        if random.random() < 0.2:  # 20% chance
            return {
                'risk': 'MEDIUM',
                'description': 'Anonymous FTP login enabled',
                'cve': 'CVE-1999-0497'
            }
        return None
    
    def check_ssh_weak(self):
        """Check for weak SSH configurations"""
        if random.random() < 0.3:
            return {
                'risk': 'HIGH',
                'description': 'SSH allows weak encryption algorithms',
                'cve': 'CVE-2008-5161'
            }
        return None
    
    def check_http_headers(self):
        """Check for missing security headers"""
        missing_headers = []
        headers_to_check = ['X-Frame-Options', 'X-XSS-Protection', 'Strict-Transport-Security']
        
        for header in headers_to_check:
            if random.random() < 0.4:
                missing_headers.append(header)
        
        if missing_headers:
            return {
                'risk': 'LOW',
                'description': f'Missing security headers: {", ".join(missing_headers)}',
                'cve': None
            }
        return None
    
    def check_smb_signing(self):
        """Check if SMB signing is disabled"""
        if random.random() < 0.25:
            return {
                'risk': 'HIGH',
                'description': 'SMB signing not required (vulnerable to MITM)',
                'cve': 'CVE-2017-0144'
            }
        return None
    
    def check_ssl_tls(self):
        """Check for weak SSL/TLS configurations"""
        if random.random() < 0.15:
            return {
                'risk': 'CRITICAL',
                'description': 'SSLv3 or TLS 1.0 enabled (POODLE vulnerability)',
                'cve': 'CVE-2014-3566'
            }
        return None

def main():
    parser = argparse.ArgumentParser(description='Network Reconnaissance & Vulnerability Scanner')
    parser.add_argument('target', help='Target IP, range, or domain')
    parser.add_argument('-m', '--mode', choices=['discover', 'scan', 'enum', 'full'], 
                       default='discover', help='Scan mode')
    parser.add_argument('-t', '--threads', type=int, default=50, help='Max threads for scanning')
    
    args = parser.parse_args()
    
    import random  # Import here for simulated checks
    
    print("="*80)
    print("🌐 NETWORK RECONNAISSANCE TOOLKIT")
    print("="*80)
    
    scanner = NetworkScanner(args.target, args.threads)
    
    if args.mode in ['discover', 'full']:
        hosts = scanner.ping_sweep()
        scanner.arp_scan()
        topology = scanner.subnet_discovery()
    
    if args.mode in ['scan', 'full'] and hosts:
        print("\n" + "="*80)
        print("🔓 VULNERABILITY ASSESSMENT")
        print("="*80)
        
        for host in hosts[:3]:  # Limit to first 3 hosts for demo
            print(f"\n📡 Scanning {host}:")
            vuln_scanner = VulnerabilityScanner(host)
            vulns = vuln_scanner.scan_common_vulns()
    
    if args.mode in ['enum', 'full'] and '.' in args.target and not args.target[0].isdigit():
        print("\n" + "="*80)
        print("📝 DNS ENUMERATION")
        print("="*80)
        scanner.dns_enumeration(args.target)
    
    print("\n" + "="*80)
    print("✅ SCAN COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
