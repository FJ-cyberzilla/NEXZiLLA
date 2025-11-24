#!/usr/bin/env python3
import os
import sys
import json
import asyncio
import aiohttp
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from pathlib import Path
import subprocess
import ipaddress
import dns.resolver
import whois
import ssl
import socket
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('CyberNexus')

class CyberNexusTerminal:
    def __init__(self):
        self.session = None
        self.command_history = []
        
        # Real agent endpoints
        self.agents = {
            'threat_intel': 'http://localhost:8001/analyze',
            'network_analyzer': 'http://localhost:8002/scan',
            'malware_analyzer': 'http://localhost:8003/analyze',
            'vuln_scanner': 'http://localhost:8004/scan',
            'osint_collector': 'http://localhost:8005/collect',
            'incident_tracker': 'http://localhost:8006/track',
            'threat_forecaster': 'http://localhost:8008/forecast'
        }
        
        self.print_banner()

    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                   CYBER INTELLIGENCE TERMINAL               ║
║                     PRODUCTION READY v3.0                   ║
╚══════════════════════════════════════════════════════════════╝

[SYSTEM] Initializing real-time threat intelligence...
[SYSTEM] Loading production analysis modules...
[SYSTEM] Terminal ready for operational use

WARNING: This system performs live analysis. Use responsibly.
"""
        print(banner)

    async def execute_command(self, command: str):
        """Execute production commands"""
        parts = command.strip().split()
        if not parts:
            return

        cmd = parts[0].lower()
        args = parts[1:]

        print(f"[CMD] {command}")

        try:
            if cmd in ['help', '?']:
                self.show_help()
                
            elif cmd == 'scan':
                await self.network_scan(args)
                
            elif cmd == 'analyze':
                await self.threat_analysis(args)
                
            elif cmd == 'whois':
                await self.whois_lookup(args)
                
            elif cmd == 'dns':
                await self.dns_analysis(args)
                
            elif cmd == 'ssl':
                await self.ssl_analysis(args)
                
            elif cmd == 'portscan':
                await self.port_scan(args)
                
            elif cmd == 'geoip':
                await self.geoip_lookup(args)
                
            elif cmd == 'malware':
                await self.malware_analysis(args)
                
            elif cmd == 'vulnscan':
                await self.vulnerability_scan(args)
                
            elif cmd == 'forecast':
                await self.threat_forecast(args)
                
            elif cmd == 'osint':
                await self.osint_collect(args)
                
            elif cmd == 'incident':
                await self.incident_analysis(args)
                
            elif cmd == 'export':
                await self.export_data(args)
                
            elif cmd == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                self.print_banner()
                
            elif cmd in ['exit', 'quit']:
                sys.exit(0)
                
            else:
                print(f"[ERROR] Unknown command: {cmd}")

        except Exception as e:
            print(f"[ERROR] Command failed: {str(e)}")

    async def network_scan(self, args):
        """Perform actual network reconnaissance"""
        if not args:
            print("[USAGE] scan <ip/domain>")
            return

        target = args[0]
        print(f"[SCAN] Starting network analysis for: {target}")

        try:
            # Resolve domain to IP
            ip = await self.resolve_domain(target)
            print(f"[SCAN] Resolved IP: {ip}")

            # Basic port scan
            open_ports = await self.quick_port_scan(ip)
            print(f"[SCAN] Open ports: {', '.join(map(str, open_ports)) if open_ports else 'None'}")

            # Service detection
            services = await self.detect_services(ip, open_ports)
            for port, service in services.items():
                print(f"[SCAN] Port {port}: {service}")

        except Exception as e:
            print(f"[SCAN_ERROR] {str(e)}")

    async def resolve_domain(self, domain: str) -> str:
        """Resolve domain to IP address"""
        try:
            return socket.gethostbyname(domain)
        except socket.gaierror:
            # Assume it's already an IP
            return domain

    async def quick_port_scan(self, ip: str, ports: List[int] = None) -> List[int]:
        """Scan common ports"""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 443, 993, 995, 3389]

        open_ports = []
        
        async def check_port(port):
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(ip, port),
                    timeout=2.0
                )
                writer.close()
                await writer.wait_closed()
                return port
            except:
                return None

        tasks = [check_port(port) for port in ports]
        results = await asyncio.gather(*tasks)
        
        return [port for port in results if port is not None]

    async def detect_services(self, ip: str, ports: List[int]) -> Dict[int, str]:
        """Detect services on open ports"""
        service_map = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 443: "HTTPS",
            993: "IMAPS", 995: "POP3S", 3389: "RDP"
        }
        
        return {port: service_map.get(port, "Unknown") for port in ports}

    async def threat_analysis(self, args):
        """Perform real threat intelligence analysis"""
        if not args:
            print("[USAGE] analyze <ip/domain/hash>")
            return

        target = args[0]
        print(f"[THREAT] Analyzing: {target}")

        # Check if it's an IP, domain, or hash
        if self.is_ip_address(target):
            await self.analyze_ip(target)
        elif self.is_domain(target):
            await self.analyze_domain(target)
        elif self.is_hash(target):
            await self.analyze_hash(target)
        else:
            print("[ERROR] Invalid target format")

    def is_ip_address(self, target: str) -> bool:
        try:
            ipaddress.ip_address(target)
            return True
        except:
            return False

    def is_domain(self, target: str) -> bool:
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$'
        return bool(re.match(domain_pattern, target))

    def is_hash(self, target: str) -> bool:
        hash_patterns = [
            r'^[a-fA-F0-9]{32}$',  # MD5
            r'^[a-fA-F0-9]{40}$',  # SHA-1
            r'^[a-fA-F0-9]{64}$',  # SHA-256
        ]
        return any(re.match(pattern, target) for pattern in hash_patterns)

    async def analyze_ip(self, ip: str):
        """Analyze IP address for threats"""
        print(f"[IP_ANALYSIS] Performing IP reputation check: {ip}")
        
        # Check blacklists
        blacklists = await self.check_ip_blacklists(ip)
        if blacklists:
            print(f"[THREAT] IP found in {len(blacklists)} blacklist(s)")
            for bl in blacklists:
                print(f"  - {bl}")
        else:
            print("[CLEAN] IP not found in common blacklists")

        # GeoIP lookup
        geo_info = await self.geoip_lookup([ip])
        if geo_info:
            print(f"[GEO] Location: {geo_info}")

    async def check_ip_blacklists(self, ip: str) -> List[str]:
        """Check IP against common blacklists"""
        blacklists = []
        
        # Common RBLs (be respectful with requests)
        rbls = [
            "zen.spamhaus.org",
            "b.barracudacentral.org"
        ]
        
        for rbl in rbls:
            try:
                query = ".".join(reversed(ip.split("."))) + f".{rbl}"
                socket.gethostbyname(query)
                blacklists.append(rbl)
            except socket.gaierror:
                continue
                
        return blacklists

    async def whois_lookup(self, args):
        """Perform WHOIS lookup"""
        if not args:
            print("[USAGE] whois <domain/ip>")
            return

        target = args[0]
        print(f"[WHOIS] Querying: {target}")

        try:
            whois_info = whois.whois(target)
            print(f"[WHOIS] Domain: {whois_info.domain_name}")
            print(f"[WHOIS] Registrar: {whois_info.registrar}")
            print(f"[WHOIS] Creation Date: {whois_info.creation_date}")
            print(f"[WHOIS] Expiration Date: {whois_info.expiration_date}")
            if whois_info.name_servers:
                print(f"[WHOIS] Name Servers: {', '.join(whois_info.name_servers)}")
            else:
                print("[WHOIS] Name Servers: N/A")
        except Exception as e:
            print(f"[WHOIS_ERROR] {str(e)}")

    async def dns_analysis(self, args):
        """Perform DNS analysis"""
        if not args:
            print("[USAGE] dns <domain>")
            return

        domain = args[0]
        print(f"[DNS] Analyzing: {domain}")

        try:
            # Common record types
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
            
            for rtype in record_types:
                try:
                    answers = dns.resolver.resolve(domain, rtype)
                    for rdata in answers:
                        print(f"[DNS] {rtype}: {rdata}")
                except:
                    continue
                    
        except Exception as e:
            print(f"[DNS_ERROR] {str(e)}")

    async def ssl_analysis(self, args):
        """Analyze SSL certificate"""
        if not args:
            print("[USAGE] ssl <domain>")
            return

        domain = args[0]
        print(f"[SSL] Analyzing certificate for: {domain}")

        try:
            context = ssl.create_default_context()
            # Enforce minimum TLS 1.2 for secure connections
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    print(f"[SSL] Subject: {cert['subject']}")
                    print(f"[SSL] Issuer: {cert['issuer']}")
                    print(f"[SSL] Valid From: {cert['notBefore']}")
                    print(f"[SSL] Valid Until: {cert['notAfter']}")
                    
                    # Check expiration
                    expires = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_left = (expires - datetime.now()).days
                    print(f"[SSL] Days until expiration: {days_left}")
                    
        except Exception as e:
            print(f"[SSL_ERROR] {str(e)}")

    async def geoip_lookup(self, args):
        """Perform GeoIP lookup"""
        if not args:
            print("[USAGE] geoip <ip>")
            return None

        ip = args[0]
        print(f"[GEOIP] Looking up: {ip}")

        try:
            # Using ipapi.co (free tier)
            response = requests.get(f"http://ipapi.co/{ip}/json/", timeout=10)
            data = response.json()
            
            if 'error' not in data:
                country = data.get('country_name', 'N/A')
                region = data.get('region', 'N/A')
                city = data.get('city', 'N/A')
                isp = data.get('org', 'N/A')
                
                print(f"[GEOIP] Country: {country}")
                print(f"[GEOIP] Region: {region}")
                print(f"[GEOIP] City: {city}")
                print(f"[GEOIP] ISP: {isp}")
                return data
            else:
                print("[GEOIP] Lookup failed")
                return None
                
        except Exception as e:
            print(f"[GEOIP_ERROR] {str(e)}")
            return None

    async def malware_analysis(self, args):
        """Analyze potential malware"""
        if not args:
            print("[USAGE] malware <file/hash/url>")
            return

        target = args[0]
        print(f"[MALWARE] Analyzing: {target}")

        # Hash analysis
        if self.is_hash(target):
            await self.analyze_hash(target)
        # URL analysis
        elif target.startswith('http'):
            await self.analyze_url(target)
        else:
            print("[ERROR] Provide a file hash or URL")

    async def analyze_hash(self, hash_str: str):
        """Analyze file hash against threat intelligence"""
        print(f"[HASH] Checking: {hash_str}")
        
        # VirusTotal API (you need to set VIRUSTOTAL_API_KEY)
        vt_key = os.getenv('VIRUSTOTAL_API_KEY')
        if vt_key:
            try:
                response = requests.get(
                    'https://www.virustotal.com/vtapi/v2/file/report',
                    params={'apikey': vt_key, 'resource': hash_str},
                    timeout=10
                )
                data = response.json()
                
                if data.get('response_code') == 1:
                    positives = data.get('positives', 0)
                    total = data.get('total', 1)
                    print(f"[VT] Detection: {positives}/{total} engines")
                    
                    if positives > 0:
                        print("[THREAT] Malicious file detected!")
                    else:
                        print("[CLEAN] No threats detected")
                else:
                    print("[VT] Hash not found in database")
                    
            except Exception as e:
                print(f"[VT_ERROR] {str(e)}")
        else:
            print("[INFO] Set VIRUSTOTAL_API_KEY for hash analysis")

    async def analyze_url(self, url: str):
        """Analyze URL for threats"""
        print(f"[URL] Analyzing: {url}")
        
        # Basic URL safety checks
        suspicious_patterns = [
            r'\.(exe|zip|rar|scr|bat|cmd)$',
            r'https?://[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',
            r'(phish|malware|virus|trojan)',
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                print(f"[SUSPICIOUS] Pattern detected: {pattern}")

    async def vulnerability_scan(self, args):
        """Perform vulnerability assessment"""
        if not args:
            print("[USAGE] vulnscan <target>")
            return

        target = args[0]
        print(f"[VULN] Scanning: {target}")

        # Check common vulnerabilities
        print("[VULN] Checking for common web vulnerabilities...")
        
        # Check HTTP security headers
        await self.check_security_headers(target)
        
        # Check for exposed services
        await self.check_exposed_services(target)

    async def check_security_headers(self, target: str):
        """Check HTTP security headers"""
        try:
            if not target.startswith('http'):
                target = f'http://{target}'
                
            response = requests.get(target, timeout=10, allow_redirects=True)
            headers = response.headers
            
            security_headers = [
                'Content-Security-Policy',
                'X-Frame-Options', 
                'X-Content-Type-Options',
                'Strict-Transport-Security',
                'X-XSS-Protection'
            ]
            
            for header in security_headers:
                if header in headers:
                    print(f"[SECURITY] ✓ {header}: {headers[header]}")
                else:
                    print(f"[WARNING] ✗ {header} missing")
                    
        except Exception as e:
            print(f"[HEADER_CHECK_ERROR] {str(e)}")

    async def threat_forecast(self, args):
        """Get threat forecast"""
        if not args:
            print("[USAGE] forecast <target> [days]")
            return

        target = args[0]
        days = int(args[1]) if len(args) > 1 else 30
        forecast_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        
        print(f"[FORECAST] Generating threat forecast for {target} on {forecast_date}")
        
        try:
            response = requests.post(
                self.agents['threat_forecaster'],
                json={
                    'target': target,
                    'forecast_date': forecast_date,
                    'query': 'threat landscape analysis'
                },
                timeout=30
            )
            
            if response.status_code == 200:
                forecast = response.json()
                print(f"[FORECAST] Predicted Risk: {forecast.get('predicted_risk_level', 0):.0%}")
                print(f"[FORECAST] Confidence: {forecast.get('confidence_score', 0):.0%}")
                
                if forecast.get('confirmed_threats'):
                    print("[FORECAST] Confirmed Threats:")
                    for threat in forecast['confirmed_threats']:
                        print(f"  - {threat}")
            else:
                print("[FORECAST_ERROR] Failed to get forecast")
                
        except Exception as e:
            print(f"[FORECAST_ERROR] {str(e)}")

    async def osint_collect(self, args):
        """Collect OSINT data"""
        if not args:
            print("[USAGE] osint <target>")
            return

        target = args[0]
        print(f"[OSINT] Collecting intelligence for: {target}")
        
        # Perform multiple OSINT techniques
        await self.whois_lookup([target])
        await self.dns_analysis([target])
        await self.ssl_analysis([target])

    async def incident_analysis(self, args):
        """Analyze security incident"""
        if not args:
            print("[USAGE] incident <incident_id>")
            return

        incident_id = args[0]
        print(f"[INCIDENT] Analyzing incident: {incident_id}")
        
        # This would integrate with your incident management system
        print("[INCIDENT] Incident analysis framework ready")
        print("[INCIDENT] Use specific incident commands for detailed analysis")

    async def export_data(self, args):
        """Export analysis data"""
        if not args:
            print("[USAGE] export <format> [filename]")
            return

        export_format = args[0]
        filename = args[1] if len(args) > 1 else f"cyber_intel_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_format}"
        
        print(f"[EXPORT] Exporting data as {export_format} to {filename}")
        print("[EXPORT] Export functionality would save current session data")

    def show_help(self):
        """Display help"""
        help_text = """
PRODUCTION COMMANDS:

NETWORK ANALYSIS:
  scan <target>        Network reconnaissance
  portscan <target>    Port scanning
  dns <domain>         DNS record analysis
  whois <domain/ip>    WHOIS lookup
  ssl <domain>         SSL certificate analysis
  geoip <ip>           GeoIP location lookup

THREAT ANALYSIS:
  analyze <target>     Comprehensive threat analysis
  malware <hash/url>   Malware analysis
  vulnscan <target>    Vulnerability assessment
  forecast <target>    Threat forecasting

OSINT & INTELLIGENCE:
  osint <target>       Open source intelligence
  incident <id>        Incident analysis

DATA MANAGEMENT:
  export <format>      Export results
  clear               Clear terminal
  help               Show this help
  exit               Exit terminal

EXAMPLES:
  scan example.com
  analyze 192.168.1.1
  whois example.com
  malware <file_hash>
  vulnscan target.com
  forecast example.com 30
"""
        print(help_text)

    async def run(self):
        """Main terminal loop"""
        while True:
            try:
                command = input("cyberintel> ").strip()
                if command:
                    await self.execute_command(command)
            except KeyboardInterrupt:
                print("\n[INFO] Use 'exit' to quit")
            except EOFError:
                break
            except Exception as e:
                print(f"[SYSTEM_ERROR] {str(e)}")

async def main():
    terminal = CyberNexusTerminal()
    await terminal.run()

if __name__ == "__main__":
    # Check Python syntax before running
    try:
        with open(__file__, 'r') as f:
            compile(f.read(), __file__, 'exec')
        print("✅ Syntax check passed")
        asyncio.run(main())
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        sys.exit(1)
