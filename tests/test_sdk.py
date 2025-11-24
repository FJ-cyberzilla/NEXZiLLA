import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from cyber_intel_sdk import CyberIntelSDK, AsyncCyberIntelSDK
from cyber_intel_sdk.models import ThreatIntel, ThreatForecast, ThreatLevel

class TestCyberIntelSDK:
    """Test Cyber Intelligence SDK"""
    
    @pytest.mark.asyncio
    async def test_sdk_initialization(self):
        """Test SDK can be initialized"""
        sdk = CyberIntelSDK(base_url="http://localhost:8007")
        assert sdk.base_url == "http://localhost:8007"
        assert sdk.api_key is None
        
    @pytest.mark.asyncio
    async def test_sdk_with_api_key(self):
        """Test SDK with API key"""
        sdk = CyberIntelSDK(base_url="http://localhost:8007", api_key="test-key")
        assert sdk.api_key == "test-key"
        
    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test async context manager"""
        async with AsyncCyberIntelSDK() as sdk:
            assert isinstance(sdk, CyberIntelSDK)
            assert sdk.session is not None
            
    @pytest.mark.asyncio
    async def test_analyze_threat_success(self, mock_session, sample_threat_data):
        """Test successful threat analysis"""
        with patch('aiohttp.ClientSession', return_value=mock_session):
            async with AsyncCyberIntelSDK() as sdk:
                # Mock the response
                mock_response = AsyncMock()
                mock_response.status = 200
                mock_response.json.return_value = sample_threat_data
                mock_session.post.return_value.__aenter__.return_value = mock_response
                
                result = await sdk.analyze_threat("test-domain.com")
                assert isinstance(result, ThreatIntel)
                assert result.target == "malicious-domain.com"
                assert result.threat_level == ThreatLevel.HIGH
                
    @pytest.mark.asyncio
    async def test_forecast_threats_success(self, mock_session, sample_forecast_data):
        """Test successful threat forecasting"""
        with patch('aiohttp.ClientSession', return_value=mock_session):
            async with AsyncCyberIntelSDK() as sdk:
                # Mock the response
                mock_response = AsyncMock()
                mock_response.status = 200
                mock_response.json.return_value = sample_forecast_data
                mock_session.post.return_value.__aenter__.return_value = mock_response
                
                result = await sdk.forecast_threats("test-domain.com")
                assert isinstance(result, ThreatForecast)
                assert result.target == "example.com"
                assert result.predicted_risk == 0.75
                
    @pytest.mark.asyncio
    async def test_analyze_threat_failure(self, mock_session):
        """Test threat analysis failure"""
        with patch('aiohttp.ClientSession', return_value=mock_session):
            async with AsyncCyberIntelSDK() as sdk:
                # Mock failed response
                mock_response = AsyncMock()
                mock_response.status = 500
                mock_session.post.return_value.__aenter__.return_value = mock_response
                
                with pytest.raises(Exception, match="Threat analysis failed"):
                    await sdk.analyze_threat("test-domain.com")
                    
    @pytest.mark.asyncio
    async def test_network_scan(self, mock_session):
        """Test network scanning"""
        with patch('aiohttp.ClientSession', return_value=mock_session):
            async with AsyncCyberIntelSDK() as sdk:
                scan_data = {
                    "target": "192.168.1.1",
                    "open_ports": [80, 443, 22],
                    "services": {"80": "HTTP", "443": "HTTPS", "22": "SSH"}
                }
                
                mock_response = AsyncMock()
                mock_response.status = 200
                mock_response.json.return_value = scan_data
                mock_session.post.return_value.__aenter__.return_value = mock_response
                
                result = await sdk.scan_network("192.168.1.1")
                assert result["target"] == "192.168.1.1"
                assert 80 in result["open_ports"]
