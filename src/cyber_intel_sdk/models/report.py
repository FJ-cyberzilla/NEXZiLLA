from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class IntelligenceReport:
    report_id: str
    report_type: str
    title: str
    timestamp: datetime
    summary: str
    severity: str
    sections: Dict[str, str]
    attachments: Dict[str, List[str]]
    metadata: Dict[str, any]
    
    def to_dict(self) -> Dict:
        return {
            "report_id": self.report_id,
            "type": self.report_type,
            "title": self.title,
            "timestamp": self.timestamp.isoformat(),
            "summary": self.summary,
            "severity": self.severity,
            "sections": self.sections,
            "attachments": self.attachments,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'IntelligenceReport':
        return cls(
            report_id=data['report_id'],
            report_type=data['type'],
            title=data['title'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            summary=data['summary'],
            severity=data['severity'],
            sections=data.get('sections', {}),
            attachments=data.get('attachments', {}),
            metadata=data.get('metadata', {})
        )
