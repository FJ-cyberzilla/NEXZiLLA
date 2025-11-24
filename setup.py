#!/usr/bin/env python3
"""
Cyber Intelligence Platform - Installation Script
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
import urllib.request
import json

class CyberIntelInstaller:
    def __init__(self):
        self.platform_dir = Path(__file__).parent
        self.install_dir = self.platform_dir / "cyber_intel_platform"
        self.requirements_file = self.platform_dir / "requirements.txt"
        self.config_dir = self.install_dir / "config"
        
    def check_prerequisites(self):
        """Check system prerequisites"""
        print("🔍 Checking system prerequisites...")
        
        # Python version check
        if sys.version_info < (3, 8):
            print("❌ Python 3.8 or higher required")
            return False
        
        # Platform check
        system = platform.system().lower()
        if system not in ['windows', 'linux', 'darwin']:
            print("❌ Unsupported operating system")
            return False
            
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
        print(f"✅ Platform: {platform.system()} {platform.release()}")
        return True
    
    def create_directory_structure(self):
        """Create necessary directories"""
        print("📁 Creating directory structure...")
        
        directories = [
            self.install_dir,
            self.config_dir,
            self.install_dir / "agents",
            self.install_dir / "logs",
            self.install_dir / "data",
            self.install_dir / "reports"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created {directory}")
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("📦 Installing dependencies...")
        
        if not self.requirements_file.exists():
            print("❌ requirements.txt not found")
            return False
        
        try:
            # Install base requirements
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)
            ])
            
            # Install additional security packages
            security_packages = [
                "python-whois",
                "dnspython",
                "requests",
                "aiohttp",
                "pyyaml",
                "colorama"
            ]
            
            for package in security_packages:
                try:
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", package
                    ])
                    print(f"  ✅ Installed {package}")
                except subprocess.CalledProcessError:
                    print(f"  ⚠️  Failed to install {package}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Dependency installation failed: {e}")
            return False
    
    def create_config_files(self):
        """Create configuration files"""
        print("⚙️ Creating configuration files...")
        
        # Default configuration
        default_config = {
            "supervisor": {
                "host": "localhost",
                "port": 8007,
                "log_level": "INFO"
            },
            "agents": {
                "threat_intel": {"port": 8001, "enabled": True},
                "network_analyzer": {"port": 8002, "enabled": True},
                "malware_detector": {"port": 8003, "enabled": True},
                "vuln_scanner": {"port": 8004, "enabled": True},
                "forecaster": {"port": 8005, "enabled": True},
                "reporter": {"port": 8006, "enabled": True},
                "validator": {"port": 8007, "enabled": True}
            },
            "api_keys": {
                "virustotal": "YOUR_VIRUSTOTAL_API_KEY",
                "abuseipdb": "YOUR_ABUSEIPDB_API_KEY",
                "shodan": "YOUR_SHODAN_API_KEY",
                "alienvault": "YOUR_ALIENVAULT_API_KEY"
            },
            "settings": {
                "max_workers": 5,
                "request_timeout": 30,
                "enable_auto_restart": True,
                "health_check_interval": 60
            }
        }
        
        config_file = self.config_dir / "default_config.yaml"
        with open(config_file, 'w') as f:
            import yaml
            yaml.dump(default_config, f, default_flow_style=False)
        
        print(f"  ✅ Created {config_file}")
        
        # Environment template
        env_template = """# Cyber Intelligence Platform Environment Variables
# Add your API keys below:

# VirusTotal API Key (Required for hash/URL analysis)
VIRUSTOTAL_API_KEY=your_virustotal_api_key_here

# AbuseIPDB API Key (Required for IP reputation)
ABUSEIPDB_API_KEY=your_abuseipdb_api_key_here

# Shodan API Key (Optional - for network intelligence)
SHODAN_API_KEY=your_shodan_api_key_here

# AlienVault OTX API Key (Optional - for threat intelligence)
ALIENVAULT_API_KEY=your_alienvault_api_key_here

# Hirschy Management AI (Optional - for advanced orchestration)
HIRSCHY_API_KEY=your_hirschy_api_key_here
HIRSCHY_API_URL=https://api.hirschy-management.ai

# Platform Settings
LOG_LEVEL=INFO
MAX_CONCURRENT_ANALYSIS=5
ENABLE_AUTO_OPTIMIZATION=true
"""
        
        env_file = self.install_dir / ".env.template"
        with open(env_file, 'w') as f:
            f.write(env_template)
        
        print(f"  ✅ Created {env_file}")
    
    def download_external_resources(self):
        """Download external resources and threat intelligence feeds"""
        print("🌐 Downloading external resources...")
        
        # Threat intelligence feeds
        ti_feeds = [
            "https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt",
            "https://feodotracker.abuse.ch/downloads/ipblocklist.txt",
            "https://rules.emergingthreats.net/blockrules/compromised-ips.txt"
        ]
        
        ti_dir = self.install_dir / "data" / "threat_intel"
        ti_dir.mkdir(parents=True, exist_ok=True)
        
        for feed_url in ti_feeds:
            try:
                filename = feed_url.split('/')[-1]
                filepath = ti_dir / filename
                
                urllib.request.urlretrieve(feed_url, filepath)
                print(f"  ✅ Downloaded {filename}")
                
            except Exception as e:
                print(f"  ⚠️  Failed to download {feed_url}: {e}")
    
    def generate_api_links(self):
        """Generate API registration links"""
        print("🔗 Generating API registration links...")
        
        api_links = {
            "VirusTotal": "https://www.virustotal.com/gui/join-us",
            "AbuseIPDB": "https://www.abuseipdb.com/register",
            "Shodan": "https://account.shodan.io/register",
            "AlienVault OTX": "https://otx.alienvault.com/api/",
            "Threat Crowd": "https://www.threatcrowd.org/",
            "CIRCL PDNS": "https://www.circl.lu/services/passive-dns/",
            "GreyNoise": "https://www.greynoise.io/",
            "Hybrid Analysis": "https://www.hybrid-analysis.com/signup"
        }
        
        links_file = self.install_dir / "API_REGISTRATION_LINKS.md"
        with open(links_file, 'w') as f:
            f.write("# 🔗 External API Registration Links\n\n")
            f.write("Register for these APIs to enhance your cyber intelligence platform:\n\n")
            
            for service, url in api_links.items():
                f.write(f"## {service}\n")
                f.write(f"- **Registration URL**: {url}\n")
                f.write(f"- **Purpose**: {' | '.join(self.get_api_purpose(service))}\n")
                f.write(f"- **Free Tier**: {self.get_free_tier_info(service)}\n\n")
        
        print(f"  ✅ Created API registration guide: {links_file}")
        
        # Print quick access links
        print("\n🎯 QUICK API REGISTRATION LINKS:")
        for service, url in api_links.items():
            print(f"   {service}: {url}")
    
    def get_api_purpose(self, service):
        """Get API purposes for documentation"""
        purposes = {
            "VirusTotal": ["File hash analysis", "URL scanning", "IP reputation"],
            "AbuseIPDB": ["IP reputation", "Threat intelligence", "Abuse reporting"],
            "Shodan": ["Network intelligence", "Device discovery", "Vulnerability data"],
            "AlienVault OTX": ["Threat indicators", "Pulse analysis", "Malware information"]
        }
        return purposes.get(service, ["Threat intelligence"])
    
    def get_free_tier_info(self, service):
        """Get free tier information"""
        free_tiers = {
            "VirusTotal": "4 requests/minute, 500/day",
            "AbuseIPDB": "1,000 requests/day",
            "Shodan": "1 request/minute, limited results",
            "AlienVault OTX": "Unlimited, rate limited"
        }
        return free_tiers.get(service, "Check website")
    
    def run_health_check(self):
        """Run initial health check"""
        print("🏥 Running health check...")
        
        try:
            # Test Python imports
            test_imports = [
                "requests", "aiohttp", "yaml", "json", 
                "asyncio", "logging", "datetime"
            ]
            
            for import_name in test_imports:
                __import__(import_name)
                print(f"  ✅ {import_name} import successful")
            
            # Test directory structure
            required_dirs = [
                self.install_dir, self.config_dir,
                self.install_dir / "agents",
                self.install_dir / "data" / "threat_intel"
            ]
            
            for directory in required_dirs:
                if directory.exists():
                    print(f"  ✅ Directory exists: {directory}")
                else:
                    print(f"  ❌ Missing directory: {directory}")
                    return False
            
            return True
            
        except ImportError as e:
            print(f"  ❌ Import failed: {e}")
            return False
    
    def display_success_message(self):
        """Display success message with next steps"""
        print("\n" + "="*60)
        print("🎉 CYBER INTELLIGENCE PLATFORM INSTALLED SUCCESSFULLY!")
        print("="*60)
        
        print("\n📋 NEXT STEPS:")
        print("1. Configure API keys:")
        print("   cp .env.template .env")
        print("   # Edit .env with your API keys")
        
        print("\n2. Start the platform:")
        print("   python orchestrator.py")
        
        print("\n3. Access the interface:")
        print("   CLI: python cyber_intel.py")
        print("   Web: http://localhost:8007 (when supervisor is running)")
        
        print("\n4. Register for external APIs:")
        print("   Check API_REGISTRATION_LINKS.md for registration URLs")
        
        print("\n🛠️ TROUBLESHOOTING:")
        print("   - Run health check: python scripts/health_check.py")
        print("   - Check logs: tail -f logs/cyber_intel.log")
        print("   - Reset configuration: python scripts/setup_environment.py --reset")
        
        print(f"\n📁 Installation directory: {self.install_dir}")
        print("🔗 API Registration Guide: API_REGISTRATION_LINKS.md")
    
    def install(self):
        """Main installation method"""
        print("🚀 Starting Cyber Intelligence Platform Installation...")
        
        try:
            if not self.check_prerequisites():
                sys.exit(1)
            
            self.create_directory_structure()
            
            if not self.install_dependencies():
                print("⚠️  Some dependencies failed to install. Platform may have limited functionality.")
            
            self.create_config_files()
            self.download_external_resources()
            self.generate_api_links()
            
            if self.run_health_check():
                self.display_success_message()
            else:
                print("❌ Health check failed. Please check the installation.")
                
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    installer = CyberIntelInstaller()
    installer.install()
