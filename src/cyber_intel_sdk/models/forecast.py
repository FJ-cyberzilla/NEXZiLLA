from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime
from .threat import ThreatLevel

@dataclass
class ThreatForecast:
    target: str
    forecast_date: str
    predicted_risk: float
    confidence: float
    current_risk: float
    confirmed_threats: List[str]
    likely_developments: List[str]
    mitigation_recommendations: List[str]
    forecast_timestamp: datetime
    
    def to_dict(self) -> Dict:
        return {
            "target": self.target,
            "forecast_date": self.forecast_date,
            "predicted_risk": self.predicted_risk,
            "confidence": self.confidence,
            "current_risk": self.current_risk,
            "confirmed_threats": self.confirmed_threats,
            "likely_developments": self.likely_developments,
            "mitigation_recommendations": self.mitigation_recommendations,
            "forecast_timestamp": self.forecast_timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ThreatForecast':
        return cls(
            target=data['target'],
            forecast_date=data['forecast_date'],
            predicted_risk=data['predicted_risk'],
            confidence=data['confidence'],
            current_risk=data.get('current_risk', 0),
            confirmed_threats=data.get('confirmed_threats', []),
            likely_developments=data.get('likely_developments', []),
            mitigation_recommendations=data.get('mitigation_recommendations', []),
            forecast_timestamp=datetime.fromisoformat(data['forecast_timestamp'])
        )
    
    def get_predicted_threat_level(self) -> ThreatLevel:
        """Convert predicted risk to threat level"""
        if self.predicted_risk >= 0.8:
            return ThreatLevel.CRITICAL
        elif self.predicted_risk >= 0.6:
            return ThreatLevel.HIGH
        elif self.predicted_risk >= 0.4:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
