from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"

class IOCType(Enum):
    IP = "ip"
    DOMAIN = "domain"
    HASH = "hash"
    URL = "url"
    EMAIL = "email"

@dataclass
class IndicatorOfCompromise:
    value: str
    type: IOCType
    confidence: float
    source: str
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        return {
            "value": self.value,
            "type": self.type.value,
            "confidence": self.confidence,
            "source": self.source,
            "first_seen": self.first_seen.isoformat() if self.first_seen else None,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'IndicatorOfCompromise':
        return cls(
            value=data['value'],
            type=IOCType(data['type']),
            confidence=data['confidence'],
            source=data['source'],
            first_seen=datetime.fromisoformat(data['first_seen']) if data.get('first_seen') else None,
            last_seen=datetime.fromisoformat(data['last_seen']) if data.get('last_seen') else None
        )

@dataclass
class ThreatIntel:
    target: str
    threat_level: ThreatLevel
    confidence: float
    indicators: List[IndicatorOfCompromise]
    analysis_timestamp: datetime
    sources: List[str]
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "target": self.target,
            "threat_level": self.threat_level.value,
            "confidence": self.confidence,
            "indicators": [ioc.to_dict() for ioc in self.indicators],
            "analysis_timestamp": self.analysis_timestamp.isoformat(),
            "sources": self.sources,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ThreatIntel':
        return cls(
            target=data['target'],
            threat_level=ThreatLevel(data['threat_level']),
            confidence=data['confidence'],
            indicators=[IndicatorOfCompromise.from_dict(ioc) for ioc in data.get('indicators', [])],
            analysis_timestamp=datetime.fromisoformat(data['analysis_timestamp']),
            sources=data.get('sources', []),
            metadata=data.get('metadata', {})
        )
    
    def get_high_confidence_iocs(self, min_confidence: float = 0.8) -> List[IndicatorOfCompromise]:
        """Get IOCs with high confidence"""
        return [ioc for ioc in self.indicators if ioc.confidence >= min_confidence]
    
    def is_critical(self) -> bool:
        """Check if threat level is critical"""
        return self.threat_level == ThreatLevel.CRITICAL
