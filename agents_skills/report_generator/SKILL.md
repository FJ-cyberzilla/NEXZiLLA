# Report Generator Agent Skill

## Purpose
Generate comprehensive, actionable intelligence reports from cyber threat data, forecasts, and analysis results.

## Input Types
- Threat intelligence data
- Forecast predictions  
- Network scan results
- Incident data
- Validation results
- Multiple agent outputs

## Output Formats
- JSON structured reports
- Markdown executive summaries
- PDF-ready documents
- CSV data exports
- STIX/TAXII threat intelligence

## Processing Rules

### 1. Report Types
- **Executive Summary**: High-level for management (1-page max)
- **Technical Deep Dive**: Detailed for security teams
- **Threat Intelligence**: STIX-compatible for sharing
- **Incident Report**: Chronological with IOCs
- **Forecast Report**: Future threat predictions

### 2. Data Integration
- Merge data from multiple agents
- Resolve conflicts using confidence scores
- Maintain data provenance
- Preserve original timestamps

### 3. Quality Standards
- All IOCs must be validated
- Include confidence levels
- Provide actionable recommendations
- Cite intelligence sources
- Include mitigation strategies

### 4. Automation Rules
- Auto-generate when analysis completes
- Trigger on high-severity findings
- Schedule daily/weekly summary reports
- Export to SIEM/SOAR systems

## Template Structure
All reports must include:
- Executive Summary (3-5 bullet points)
- Key Findings (prioritized by severity)
- Technical Details (with evidence)
- Impact Assessment (business/technical)
- Recommended Actions (immediate/long-term)
- Intelligence Sources (attribution)
- Appendices (raw data, IOCs, logs)

## Response Format
```json
{
  "report_id": "string",
  "type": "executive|technical|threat_intel|incident|forecast",
  "title": "string",
  "timestamp": "ISO8601",
  "summary": "string",
  "severity": "low|medium|high|critical",
  "sections": {
    "executive_summary": "string",
    "key_findings": ["array"],
    "technical_analysis": "string", 
    "impact_assessment": "string",
    "recommendations": ["array"],
    "intelligence_sources": ["array"]
  },
  "attachments": {
    "iocs": ["array"],
    "raw_data": "object",
    "visualizations": ["urls"]
  },
  "metadata": {
    "generated_by": "agent_name",
    "data_sources": ["array"],
    "confidence_score": 0.0-1.0
  }
}
