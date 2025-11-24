"""
Workflow Coordination Prompts
"""

GENERATOR_PROMPT = """
You are a {agent_type} Agent. Your goal is to complete the intelligence task based on the user input.

{context}

Output your answer in the following format:

<thoughts>
[Your understanding of the task, context, and how you plan to approach it]
[Analysis of previous feedback and improvements needed]
[Your reasoning process and methodology]
</thoughts>

<response>
[Your actual intelligence output - analysis, report, data, etc.]
</response>

Task: {task}
"""

SYNTHESIS_PROMPT = """
Synthesize these specialized threat analysis results into a comprehensive assessment:

ORIGINAL THREAT: {threat_description}

SPECIALIZED ANALYSES:
{worker_results}

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

VALIDATION_PROMPT = """
Validate this cyber intelligence data:

DATA TYPE: {data_type}
DATA TO VALIDATE: {data}
VALIDATION CRITERIA: {criteria}

Return validation results:
<validation>
    <status>VALID/INVALID/UNCERTAIN</status>
    <confidence>0.0-1.0</confidence>
    <issues>["list of issues or concerns"]</issues>
    <recommendations>["validation recommendations"]</recommendations>
</validation>
"""
