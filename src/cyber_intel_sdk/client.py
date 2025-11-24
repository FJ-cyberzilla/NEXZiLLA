#!/usr/bin/env python3
import aiohttp
import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta  # ✅ Added timedelta import
from .models.threat import ThreatIntel
from .models.forecast import ThreatForecast
from .models.report import IntelligenceReport

class CyberIntelSDK:
    """Main SDK client for Cyber Intelligence Platform"""
    
    def __init__(self, base_url: str = "http://localhost:8007", api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = None
        self.agents = {}
        
    async def __aenter__(self):
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def connect(self):
        """Initialize connection to cyber intelligence platform"""
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        self.session = aiohttp.ClientSession(headers=headers)
        
        # Discover available agents
        await self.discover_agents()
    
    async def close(self):
        """Close SDK connection"""
        if self.session:
            await self.session.close()
    
    async def discover_agents(self):
        """Discover all available agents in the system"""
        try:
            async with self.session.get(f"{self.base_url}/agents") as response:
                data = await response.json()
                self.agents = data.get('agents', {})
        except Exception as e:
            print(f"Agent discovery failed: {e}")
            self.agents = {}
    
    async def analyze_threat(self, target: str, analysis_type: str = "comprehensive") -> ThreatIntel:
        """Perform threat intelligence analysis"""
        try:
            async with self.session.post(
                f"{self.base_url}/analyze",
                json={"target": target, "type": analysis_type}
            ) as response:
                data = await response.json()
                return ThreatIntel.from_dict(data)
        except Exception as e:
            raise Exception(f"Threat analysis failed: {e}")
    
    async def forecast_threats(self, target: str, forecast_date: str = None) -> ThreatForecast:
        """Get threat forecast for target"""
        if not forecast_date:
            # Default to 30 days from now
            forecast_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')  # ✅ Fixed: timedelta imported
        
        try:
            async with self.session.post(
                f"{self.base_url}/forecast",
                json={"target": target, "forecast_date": forecast_date}
            ) as response:
                data = await response.json()
                return ThreatForecast.from_dict(data)
        except Exception as e:
            raise Exception(f"Threat forecast failed: {e}")
    
    async def generate_report(self, report_data: Dict, report_type: str = "threat_intel") -> IntelligenceReport:
        """Generate intelligence report"""
        try:
            async with self.session.post(
                f"{self.base_url}/reports/generate",
                json={"data": report_data, "type": report_type}
            ) as response:
                data = await response.json()
                return IntelligenceReport.from_dict(data)
        except Exception as e:
            raise Exception(f"Report generation failed: {e}")
    
    async def scan_network(self, target: str, scan_type: str = "comprehensive") -> Dict:
        """Perform network security scan"""
        try:
            async with self.session.post(
                f"{self.base_url}/scan",
                json={"target": target, "scan_type": scan_type}
            ) as response:
                return await response.json()
        except Exception as e:
            raise Exception(f"Network scan failed: {e}")
    
    async def validate_ioc(self, ioc: str, ioc_type: str = "auto") -> Dict:
        """Validate Indicator of Compromise"""
        try:
            async with self.session.post(
                f"{self.base_url}/validate",
                json={"value": ioc, "type": ioc_type}
            ) as response:
                return await response.json()
        except Exception as e:
            raise Exception(f"IOC validation failed: {e}")
    
    async def get_system_status(self) -> Dict:
        """Get overall system status"""
        try:
            async with self.session.get(f"{self.base_url}/status") as response:
                return await response.json()
        except Exception as e:
            raise Exception(f"Status check failed: {e}")
    
    async def execute_command(self, command: str, args: Dict = None) -> Dict:
        """Execute raw command through the system"""
        try:
            async with self.session.post(
                f"{self.base_url}/execute",
                json={"command": command, "args": args or {}}
            ) as response:
                return await response.json()
        except Exception as e:
            raise Exception(f"Command execution failed: {e}")

class AsyncCyberIntelSDK:
    """Async context manager version"""
    
    def __init__(self, base_url: str = "http://localhost:8007", api_key: str = None):
        self.sdk = CyberIntelSDK(base_url, api_key)
    
    async def __aenter__(self):
        await self.sdk.connect()
        return self.sdk
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.sdk.close()

# Synchronous wrapper for convenience
class SyncCyberIntelSDK:
    """Synchronous wrapper for the SDK"""
    
    def __init__(self, base_url: str = "http://localhost:8007", api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key
        self._loop = None
    
    def _get_loop(self):
        if self._loop is None:
            try:
                self._loop = asyncio.get_event_loop()
            except RuntimeError:
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
        return self._loop
    
    def analyze_threat(self, target: str, analysis_type: str = "comprehensive") -> ThreatIntel:
        """Sync threat analysis"""
        loop = self._get_loop()
        return loop.run_until_complete(
            self._async_call('analyze_threat', target, analysis_type)
        )
    
    def forecast_threats(self, target: str, forecast_date: str = None) -> ThreatForecast:
        """Sync threat forecast"""
        loop = self._get_loop()
        return loop.run_until_complete(
            self._async_call('forecast_threats', target, forecast_date)
        )
    
    async def _async_call(self, method: str, *args, **kwargs):
        """Make async call through context manager"""
        async with AsyncCyberIntelSDK(self.base_url, self.api_key) as sdk:
            return await getattr(sdk, method)(*args, **kwargs)
