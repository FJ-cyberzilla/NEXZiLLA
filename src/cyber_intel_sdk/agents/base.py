from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime
import aiohttp

class BaseAgent(ABC):
    """Base class for all cyber intelligence agents"""
    
    def __init__(self, name: str, endpoint: str, api_key: str = None):
        self.name = name
        self.endpoint = endpoint
        self.api_key = api_key
        self.session = None
        self.metrics = {
            "requests_made": 0,
            "successful_requests": 0,
            "last_request": None
        }
    
    async def connect(self):
        """Initialize agent connection"""
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        self.session = aiohttp.ClientSession(headers=headers)
    
    async def close(self):
        """Close agent connection"""
        if self.session:
            await self.session.close()
    
    async def health_check(self) -> bool:
        """Check agent health"""
        try:
            async with self.session.get(f"{self.endpoint}/health") as response:
                return response.status == 200
        except:
            return False
    
    async def call_agent(self, endpoint: str, data: Dict = None) -> Dict:
        """Make request to agent endpoint"""
        self.metrics["requests_made"] += 1
        
        try:
            async with self.session.post(
                f"{self.endpoint}/{endpoint}",
                json=data or {}
            ) as response:
                self.metrics["last_request"] = datetime.now()
                
                if response.status == 200:
                    self.metrics["successful_requests"] += 1
                    return await response.json()
                else:
                    raise Exception(f"Agent returned status {response.status}")
        except Exception as e:
            raise Exception(f"Agent call failed: {e}")
    
    @abstractmethod
    async def process(self, data: Dict) -> Dict:
        """Process data through this agent - to be implemented by subclasses"""
        pass

class ThreatIntelAgent(BaseAgent):
    """Threat intelligence agent specialization"""
    
    async def analyze_ip(self, ip: str) -> Dict:
        """Analyze IP address for threats"""
        return await self.call_agent("analyze", {"ip": ip})
    
    async def analyze_domain(self, domain: str) -> Dict:
        """Analyze domain for threats"""
        return await self.call_agent("analyze", {"domain": domain})
    
    async def analyze_hash(self, file_hash: str) -> Dict:
        """Analyze file hash"""
        return await self.call_agent("analyze", {"hash": file_hash})
    
    async def process(self, data: Dict) -> Dict:
        return await self.analyze_ip(data.get('target'))

class ForecastAgent(BaseAgent):
    """Threat forecasting agent specialization"""
    
    async def get_forecast(self, target: str, forecast_date: str) -> Dict:
        """Get threat forecast"""
        return await self.call_agent("forecast", {
            "target": target,
            "forecast_date": forecast_date
        })
    
    async def process(self, data: Dict) -> Dict:
        return await self.get_forecast(
            data.get('target'),
            data.get('forecast_date')
        )

class ReportAgent(BaseAgent):
    """Report generation agent specialization"""
    
    async def generate_report(self, report_data: Dict, report_type: str) -> Dict:
        """Generate intelligence report"""
        return await self.call_agent("generate", {
            "data": report_data,
            "type": report_type
        })
    
    async def process(self, data: Dict) -> Dict:
        return await self.generate_report(
            data.get('report_data'),
            data.get('report_type', 'threat_intel')
        )
