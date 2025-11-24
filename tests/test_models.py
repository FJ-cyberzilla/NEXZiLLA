import pytest
from datetime import datetime
from cyber_intel_sdk.models import (
    ThreatIntel, ThreatForecast, IntelligenceReport,
    ThreatLevel, IOCType, IndicatorOfCompromise
)

class TestThreatModels:
    """Test threat intelligence models"""
    
    def test_threat_level_enum(self):
        """Test threat level enum values"""
        assert ThreatLevel.LOW.value == "low"
        assert ThreatLevel.MEDIUM.value == "medium"
        assert ThreatLevel.HIGH.value == "high"
        assert ThreatLevel.CRITICAL.value == "critical"
        
    def test_ioc_type_enum(self):
        """Test IOC type enum values"""
        assert IOCType.IP.value == "ip"
        assert IOCType.DOMAIN.value == "domain"
        assert IOCType.HASH.value == "hash"
        assert IOCType.URL.value == "url"
        assert IOCType.EMAIL.value == "email"
        
    def test_indicator_of_compromise(self):
        """Test IOC creation and serialization"""
        ioc = IndicatorOfCompromise(
            value="192.168.1.100",
            type=IOCType.IP,
            confidence=0.9,
            source="threat_feed",
            first_seen=datetime(2024, 1, 1, 12, 0, 0),
            last_seen=datetime(2024, 1, 1, 14, 0, 0)
        )
        
        # Test to_dict
        ioc_dict = ioc.to_dict()
        assert ioc_dict["value"] == "192.168.1.100"
        assert ioc_dict["type"] == "ip"
        assert ioc_dict["confidence"] == 0.9
        
        # Test from_dict
        ioc_from_dict = IndicatorOfCompromise.from_dict(ioc_dict)
        assert ioc_from_dict.value == ioc.value
        assert ioc_from_dict.type == ioc.type
        
    def test_threat_intel_creation(self):
        """Test threat intelligence creation"""
        ioc = IndicatorOfCompromise(
            value="malicious-domain.com",
            type=IOCType.DOMAIN,
            confidence=0.85,
            source="analysis"
        )
        
        threat_intel = ThreatIntel(
            target="example.com",
            threat_level=ThreatLevel.HIGH,
            confidence=0.8,
            indicators=[ioc],
            analysis_timestamp=datetime.now(),
            sources=["threat_feed", "analysis"],
            metadata={"campaign": "APT29"}
        )
        
        assert threat_intel.target == "example.com"
        assert threat_intel.threat_level == ThreatLevel.HIGH
        assert len(threat_intel.indicators) == 1
        assert threat_intel.is_critical() == False  # HIGH is not CRITICAL
        
    def test_threat_intel_critical(self):
        """Test critical threat detection"""
        threat_intel = ThreatIntel(
            target="critical-target.com",
            threat_level=ThreatLevel.CRITICAL,
            confidence=0.95,
            indicators=[],
            analysis_timestamp=datetime.now(),
            sources=[]
        )
        
        assert threat_intel.is_critical() == True
        
    def test_threat_forecast(self):
        """Test threat forecast model"""
        forecast = ThreatForecast(
            target="example.com",
            forecast_date="2024-12-01",
            predicted_risk=0.85,
            confidence=0.8,
            current_risk=0.6,
            confirmed_threats=["Ransomware campaign"],
            likely_developments=["Increased attack surface"],
            mitigation_recommendations=["Patch systems", "Backup data"],
            forecast_timestamp=datetime.now()
        )
        
        assert forecast.target == "example.com"
        assert forecast.predicted_risk == 0.85
        assert forecast.get_predicted_threat_level() == ThreatLevel.CRITICAL
        
    def test_intelligence_report(self):
        """Test intelligence report model"""
        report = IntelligenceReport(
            report_id="REP-20240101-001",
            report_type="threat_intel",
            title="Advanced Threat Analysis",
            timestamp=datetime.now(),
            summary="Comprehensive threat analysis report",
            severity="high",
            sections={
                "executive_summary": "Threat overview",
                "technical_details": "Detailed analysis"
            },
            attachments={
                "iocs": ["192.168.1.100", "malicious-domain.com"]
            },
            metadata={"analyst": "AI System", "version": "1.0"}
        )
        
        assert report.report_id == "REP-20240101-001"
        assert report.report_type == "threat_intel"
        assert "executive_summary" in report.sections
