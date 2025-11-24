"""
Evaluator Prompts for Quality Assurance
"""

THREAT_INTEL_EVALUATOR_PROMPT = """
Evaluate this threat intelligence analysis for:

1. Threat accuracy and relevance
2. IOC completeness and validity  
3. Risk assessment accuracy
4. Actionable recommendations
5. Data source credibility
6. Timeliness and context

Original task: {task}
Content to evaluate: {content}

Only output "PASS" if all criteria are met and you have no further suggestions for improvements.

<evaluation>PASS, NEEDS_IMPROVEMENT, or FAIL</evaluation>
<feedback>
Specific, actionable feedback on what needs improvement and why.
Suggestions for better analysis, data sources, or methodology.
Assessment of completeness, accuracy, and actionability.
</feedback>
"""

FORECAST_EVALUATOR_PROMPT = """
Evaluate this threat forecast for:

1. Forecast logic and reasoning
2. Risk probability accuracy
3. Trend analysis quality
4. Mitigation recommendation relevance
5. Confidence level justification
6. Historical pattern alignment

<evaluation>PASS, NEEDS_IMPROVEMENT, or FAIL</evaluation>
<feedback>
Detailed feedback on forecast quality and improvements needed.
</feedback>
"""

REPORT_EVALUATOR_PROMPT = """
Evaluate this intelligence report for:

1. Report structure and clarity
2. Executive summary quality
3. Technical detail appropriateness
4. Recommendation actionability
5. Data visualization suggestions
6. Audience targeting

<evaluation>PASS, NEEDS_IMPROVEMENT, or FAIL</evaluation>
<feedback>
Report quality assessment and improvement suggestions.
</feedback>
"""
