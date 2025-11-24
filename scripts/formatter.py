#!/usr/bin/env python3
import json
import markdown
from typing import Dict

class ReportFormatter:
    """Format reports for different output types"""
    
    @staticmethod
    def to_markdown(report: Dict) -> str:
        """Convert report to markdown format"""
        md = f"# {report['title']}\n\n"
        md += f"**Report ID**: {report['report_id']}  \n"
        md += f"**Generated**: {report['timestamp']}  \n"
        md += f"**Severity**: {report['severity'].upper()}  \n\n"
        
        # Executive Summary
        md += "## Executive Summary\n\n"
        md += f"{report['sections']['executive_summary']}\n\n"
        
        # Key Findings
        md += "## Key Findings\n\n"
        for finding in report['sections']['key_findings']:
            md += f"- {finding}\n"
        md += "\n"
        
        # Recommendations
        md += "## Recommended Actions\n\n"
        for rec in report['sections']['recommendations']:
            md += f"- {rec}\n"
        
        return md
    
    @staticmethod
    def to_json(report: Dict) -> str:
        """Convert report to formatted JSON"""
        return json.dumps(report, indent=2)
    
    @staticmethod
    def to_stix(report: Dict) -> Dict:
        """Convert to STIX 2.1 format for threat intelligence sharing"""
        # Basic STIX structure - would be expanded for production
        stix_bundle = {
            "type": "bundle",
            "id": f"bundle--{report['report_id']}",
            "objects": [
                {
                    "type": "report",
                    "id": f"report--{report['report_id']}",
                    "name": report['title'],
                    "published": report['timestamp'],
                    "object_refs": []  # Would contain STIX objects for IOCs
                }
            ]
        }
        
        # Add IOCs as STIX objects
        for ioc in report['attachments'].get('iocs', []):
            # This would be expanded to handle different IOC types
            stix_bundle['objects'].append({
                "type": "indicator",
                "id": f"indicator--{hash(ioc)}",
                "pattern": f"[ipv4-addr:value = '{ioc}']",
                "pattern_type": "stix"
            })
        
        return stix_bundle
