#!/usr/bin/env python3
import asyncio
import aiohttp
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging
from dataclasses import dataclass
import re

logger = logging.getLogger('CyberOrchestrator')

@dataclass
class AnalysisTask:
    type: str
    description: str
    priority: str = "medium"
    required_agents: List[str] = None
    
    def __post_init__(self):
        if self.required_agents is None:
            self.required_agents = []

class CyberThreatOrchestrator:
    """Dynamic orchestrator that decides which cyber agents to deploy for each threat"""
    
    def __init__(self, supervisor_url: str = "http://localhost:8007"):
        self.supervisor_url = supervisor_url
        self.session = None
        self.available_agents = [
            "threat_intel", "network_analyzer", "malware_detector", 
            "vuln_scanner", "forecaster", "reporter", "validator"
        ]
    
    async def initialize(self):
        self.session = aiohttp.ClientSession()
    
    async def close(self):
        if self.session:
            await self.session.close()
    
    def parse_tasks(self, tasks_xml: str) -> List[AnalysisTask]:
        """Parse XML tasks into structured analysis tasks"""
        tasks = []
        current_task = {}
        
        for line in tasks_xml.split("\n"):
            line = line.strip()
            if not line:
                continue
            
            if line.startswith("<task>"):
                current_task = {}
            elif line.startswith("<type>"):
                current_task["type"] = line[6:-7].strip()
            elif line.startswith("<description>"):
                current_task["description"] = line[12:-13].strip()
            elif line.startswith("<priority>"):
                current_task["priority"] = line[10:-11].strip().lower()
            elif line.startswith("<agents>"):
                agents_text = line[8:-9].strip()
                current_task["required_agents"] = [a.strip() for a in agents_text.split(",")]
            elif line.startswith("</task>"):
                if "description" in current_task:
                    task = AnalysisTask(
                        type=current_task.get("type", "analysis"),
                        description=current_task["description"],
                        priority=current_task.get("priority", "medium"),
                        required_agents=current_task.get("required_agents", [])
                    )
                    tasks.append(task)
        
        return tasks
    
    async def analyze_threat(self, threat_description: str, context: Dict = None) -> Dict:
        """Orchestrate multi-agent threat analysis"""
        context = context or {}
        
        # Step 1: Orchestrator analyzes the threat and plans the approach
        orchestrator_prompt = self._build_orchestrator_prompt(threat_description, context)
        orchestrator_response = await self._call_llm(orchestrator_prompt)
        
        analysis = self._extract_xml(orchestrator_response, "analysis")
        tasks_xml = self._extract_xml(orchestrator_response, "tasks")
        tasks = self.parse_tasks(tasks_xml)
        
        logger.info("🔍 ORCHESTRATOR THREAT ANALYSIS")
        logger.info(f"Analysis: {analysis}")
        logger.info(f"Identified {len(tasks)} analysis approaches")
        
        # Step 2: Execute tasks with specialized workers
        worker_results = await self._execute_tasks(tasks, threat_description, context)
        
        # Step 3: Synthesize results
        synthesis = await self._synthesize_results(worker_results, threat_description)
        
        return {
            "threat_analysis": analysis,
            "orchestration_plan": [task.__dict__ for task in tasks],
            "worker_results": worker_results,
            "synthesis": synthesis,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _execute_tasks(self, tasks: List[AnalysisTask], threat_description: str, context: Dict) -> List[Dict]:
        """Execute analysis tasks with specialized agents"""
        worker_results = []
        
        for i, task in enumerate(tasks, 1):
            logger.info(f"🛠️ [{i}/{len(tasks)}] Executing: {task.type}")
            
            # Build worker prompt for this specific analysis type
            worker_prompt = self._build_worker_prompt(task, threat_description, context)
            
            # Determine which agent to use
            agent_type = self._select_agent_for_task(task)
            
            try:
                # Call the appropriate agent
                worker_response = await self._call_agent(agent_type, worker_prompt)
                worker_content = self._extract_xml(worker_response, "response")
                
                if not worker_content.strip():
                    worker_content = f"[No response from {agent_type} agent]"
                
                worker_results.append({
                    "task_type": task.type,
                    "agent_used": agent_type,
                    "description": task.description,
                    "result": worker_content,
                    "priority": task.priority
                })
                
            except Exception as e:
                logger.error(f"Task execution failed: {e}")
                worker_results.append({
                    "task_type": task.type,
                    "agent_used": agent_type,
                    "description": task.description,
                    "result": f"[Execution failed: {str(e)}]",
                    "priority": task.priority,
                    "error": True
                })
        
        return worker_results
    
    def _build_orchestrator_prompt(self, threat_description: str, context: Dict) -> str:
        """Build prompt for threat analysis orchestration"""
        return f"""
You are a Cyber Threat Analysis Orchestrator. Analyze this threat scenario and determine the best analytical approaches.

THREAT SCENARIO: {threat_description}

CONTEXT: {json.dumps(context, indent=2)}

Available specialized agents:
- threat_intel: Threat intelligence and IOC analysis
- network_analyzer: Network traffic and infrastructure analysis  
- malware_detector: Malware behavior and characteristics
- vuln_scanner: Vulnerability assessment and exploit analysis
- forecaster: Threat prediction and risk trajectory
- reporter: Report generation and synthesis
- validator: Data validation and quality assurance

Analyze this threat and break it down into 2-4 distinct analytical approaches that would provide comprehensive coverage.

Return your response in this format:

<analysis>
Explain your understanding of the threat and which analytical approaches would be most valuable.
Focus on how each approach addresses different aspects of the threat.
</analysis>

<tasks>
    <task>
    <type>threat_attribution</type>
    <description>Analyze threat actor patterns, TTPs, and potential attribution</description>
    <priority>high</priority>
    <agents>threat_intel,forecaster</agents>
    </task>
    <task>
    <type>impact_assessment</type>
    <description>Evaluate potential business impact and damage assessment</description>
    <priority>medium</priority>
    <agents>reporter,validator</agents>
    </task>
</tasks>
"""
    
    def _build_worker_prompt(self, task: AnalysisTask, threat_description: str, context: Dict) -> str:
        """Build prompt for specialized worker agents"""
        return f"""
You are a specialized cyber intelligence agent focused on: {task.type}

ORIGINAL THREAT: {threat_description}
TASK TYPE: {task.type}
TASK DESCRIPTION: {task.description}
PRIORITY: {task.priority.upper()}
CONTEXT: {json.dumps(context, indent=2)}

Provide focused, expert analysis in your specialized area. Be thorough but concise.

Return your analysis in this format:

<response>
[Your specialized analysis here. Include key findings, evidence, and recommendations specific to your expertise.]
</response>
"""
    
    def _select_agent_for_task(self, task: AnalysisTask) -> str:
        """Select the most appropriate agent for a task"""
        # Use specified agents if provided
        if task.required_agents:
            return task.required_agents[0]  # Use first specified agent
        
        # Default mappings based on task type
        agent_mapping = {
            "threat_attribution": "threat_intel",
            "ioc_analysis": "threat_intel", 
            "campaign_analysis": "threat_intel",
            "network_traffic": "network_analyzer",
            "infrastructure": "network_analyzer",
            "malware_analysis": "malware_detector",
            "vulnerability": "vuln_scanner",
            "risk_forecast": "forecaster",
            "report_synthesis": "reporter",
            "data_validation": "validator"
        }
        
        return agent_mapping.get(task.type, "threat_intel")
    
    async def _synthesize_results(self, worker_results: List[Dict], threat_description: str) -> Dict:
        """Synthesize all worker results into comprehensive assessment"""
        synthesis_prompt = f"""
Synthesize these specialized threat analysis results into a comprehensive assessment:

ORIGINAL THREAT: {threat_description}

SPECIALIZED ANALYSES:
{json.dumps(worker_results, indent=2)}

Provide an executive summary that highlights:
1. Overall threat severity and confidence
2. Key findings from each analysis perspective
3. Correlations and patterns across analyses
4. Recommended immediate actions
5. Strategic recommendations

Return in JSON format:
{{
    "executive_summary": "string",
    "overall_risk_score": 0.0-1.0,
    "confidence_level": "low/medium/high",
    "key_findings": ["array"],
    "immediate_actions": ["array"],
    "strategic_recommendations": ["array"]
}}
"""
        
        try:
            synthesis_response = await self._call_llm(synthesis_prompt)
            return json.loads(synthesis_response)
        except:
            return {
                "executive_summary": "Synthesis failed - review individual analyses",
                "overall_risk_score": 0.5,
                "confidence_level": "medium",
                "key_findings": ["Review individual specialist analyses for details"],
                "immediate_actions": ["Monitor situation", "Review logs"],
                "strategic_recommendations": ["Implement defense in depth"]
            }
    
    async def _call_llm(self, prompt: str) -> str:
        """Call LLM through supervisor"""
        try:
            async with self.session.post(
                f"{self.supervisor_url}/llm/call",
                json={"prompt": prompt, "model": "claude-sonnet-4-5"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get('response', '')
                else:
                    raise Exception(f"LLM call failed with status {response.status}")
        except Exception as e:
            logger.error(f"LLM call error: {e}")
            return f"Error: {str(e)}"
    
    async def _call_agent(self, agent_type: str, prompt: str) -> str:
        """Call specialized agent through supervisor"""
        try:
            async with self.session.post(
                f"{self.supervisor_url}/agents/call",
                json={"agent": agent_type, "prompt": prompt}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get('response', '')
                else:
                    raise Exception(f"Agent call failed with status {response.status}")
        except Exception as e:
            logger.error(f"Agent call error: {e}")
            return f"Error calling {agent_type}: {str(e)}"
    
    def _extract_xml(self, text: str, tag: str) -> str:
        """Extract content from XML tags"""
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"
        
        start_idx = text.find(start_tag)
        if start_idx == -1:
            return ""
        
        start_idx += len(start_tag)
        end_idx = text.find(end_tag, start_idx)
        
        if end_idx == -1:
            return text[start_idx:].strip()
        
        return text[start_idx:end_idx].strip()

# Specialized orchestrators for different threat types
class APTOrchestrator(CyberThreatOrchestrator):
    """Specialized orchestrator for Advanced Persistent Threat analysis"""
    
    async def analyze_apt_campaign(self, indicators: List[str], target_org: str) -> Dict:
        """Orchestrate APT campaign analysis"""
        threat_description = f"""
APT Campaign Analysis Request:
- Target Organization: {target_org}
- Initial Indicators: {', '.join(indicators)}
- Analysis Focus: Campaign attribution, TTPs, infrastructure, mitigation
"""
        
        context = {
            "campaign_type": "apt",
            "target_industry": "to_be_determined", 
            "sophistication_level": "advanced",
            "response_urgency": "high"
        }
        
        return await self.analyze_threat(threat_description, context)

class IncidentResponseOrchestrator(CyberThreatOrchestrator):
    """Specialized orchestrator for incident response"""
    
    async def coordinate_incident_response(self, incident_data: Dict) -> Dict:
        """Orchestrate multi-agent incident response"""
        threat_description = f"""
INCIDENT RESPONSE: {incident_data.get('incident_type', 'Unknown')}
SEVERITY: {incident_data.get('severity', 'Unknown')}
AFFECTED SYSTEMS: {', '.join(incident_data.get('affected_systems', []))}
INITIAL INDICATORS: {incident_data.get('indicators', [])}
"""
        
        context = {
            "incident_phase": "initial_response",
            "business_impact": incident_data.get('business_impact', 'unknown'),
            "regulatory_requirements": incident_data.get('regulatory', []),
            "response_deadline": incident_data.get('response_deadline')
        }
        
        return await self.analyze_threat(threat_description, context)
