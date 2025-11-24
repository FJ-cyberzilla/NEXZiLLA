import pytest
import asyncio
from unittest.mock import patch, AsyncMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestCyberNexusTerminal:
    """Test Cyber Nexus Terminal"""
    
    @pytest.fixture
    def terminal(self):
        """Create terminal instance for testing"""
        from cyber_nexus import CyberNexusTerminal
        return CyberNexusTerminal()
    
    def test_terminal_initialization(self, terminal):
        """Test terminal initialization"""
        assert terminal.session is None
        assert terminal.command_history == []
        assert 'threat_intel' in terminal.agents
        assert 'network_analyzer' in terminal.agents
        
    def test_is_ip_address(self, terminal):
        """Test IP address validation"""
        assert terminal.is_ip_address("192.168.1.1") == True
        assert terminal.is_ip_address("255.255.255.255") == True
        assert terminal.is_ip_address("invalid-ip") == False
        assert terminal.is_ip_address("300.300.300.300") == False
        
    def test_is_domain(self, terminal):
        """Test domain validation"""
        assert terminal.is_domain("example.com") == True
        assert terminal.is_domain("sub.domain.co.uk") == True
        assert terminal.is_domain("invalid_domain") == False
        assert terminal.is_domain("http://example.com") == False
        
    def test_is_hash(self, terminal):
        """Test hash validation"""
        # MD5
        assert terminal.is_hash("d41d8cd98f00b204e9800998ecf8427e") == True
        # SHA1
        assert terminal.is_hash("da39a3ee5e6b4b0d3255bfef95601890afd80709") == True
        # SHA256
        assert terminal.is_hash("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855") == True
        # Invalid
        assert terminal.is_hash("not-a-hash") == False
        assert terminal.is_hash("123") == False
        
    @pytest.mark.asyncio
    async def test_resolve_domain(self, terminal):
        """Test domain resolution"""
        with patch('socket.gethostbyname') as mock_resolve:
            mock_resolve.return_value = "93.184.216.34"
            ip = await terminal.resolve_domain("example.com")
            assert ip == "93.184.216.34"
            
    @pytest.mark.asyncio
    async def test_resolve_domain_failure(self, terminal):
        """Test domain resolution failure"""
        with patch('socket.gethostbyname') as mock_resolve:
            mock_resolve.side_effect = socket.gaierror
            ip = await terminal.resolve_domain("invalid-domain-that-doesnt-exist.abc")
            # Should return the original input when resolution fails
            assert ip == "invalid-domain-that-doesnt-exist.abc"
