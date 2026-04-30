"""Coach Agent - Provides final feedback using ADK patterns."""
import json
from typing import Any, Dict, List
from adk_agents.base_agent import BaseInterviewAgent, AgentConfig
from google.genai import Client
import config


class CoachAgent(BaseInterviewAgent):
    """Agent that provides comprehensive coaching feedback."""
    
    def __init__(self, client: Client):
        """Initialize the Coach agent."""
        agent_config = AgentConfig(
            name="Coach",
            role="Mentor - Synthesizes feedback and provides actionable coaching",
            temperature=0.7,
            response_format="text",
            max_iterations=1,
        )
        
        system_prompt = config.load_prompt("coach.md")
        super().__init__(client, agent_config, system_prompt)
        
        # Register tools
        self.register_tool(
            "identify_skill_gaps",
            self._identify_skill_gaps,
            "Identifies specific skill gaps from interview performance"
        )
        
        self.register_tool(
            "generate_practice_plan",
            self._generate_practice_plan,
            "Generates a personalized practice plan"
        )
        
        self.register_tool(
            "benchmark_performance",
            self._benchmark_performance,
            "Benchmarks performance against role expectations"
        )
    
    def _identify_skill_gaps(
        self,
        evaluations: List[Dict[str, Any]],
        role: str,
    ) -> Dict[str, Any]:
        """Tool: Identify specific skill gaps.
        
        Args:
            evaluations: All turn evaluations
            role: Target role
            
        Returns:
            Identified skill gaps
        """
        gaps_prompt = f"""
Target Role: {role}

All Evaluations:
{json.dumps(evaluations, indent=2)}

Identify specific skill gaps:
1. Technical skills lacking
2. Behavioral competencies weak
3. Communication issues
4. Knowledge gaps
5. Experience gaps

For each gap, provide:
- Gap description
- Severity (critical/moderate/minor)
- Evidence from interview
- Impact on role success

Return as JSON.
"""
        
        response = self._generate_response(gaps_prompt, response_format="json")
        return json.loads(response)
    
    def _generate_practice_plan(
        self,
        skill_gaps: Dict[str, Any],
        role: str,
        focus_area: str,
    ) -> Dict[str, Any]:
        """Tool: Generate personalized practice plan.
        
        Args:
            skill_gaps: Identified skill gaps
            role: Target role
            focus_area: Interview focus area
            
        Returns:
            Practice plan
        """
        plan_prompt = f"""
Target Role: {role}
Focus Area: {focus_area}

Skill Gaps:
{json.dumps(skill_gaps, indent=2)}

Create a 2-week practice plan with:
1. Daily activities (30-60 min each)
2. Specific resources (articles, videos, courses)
3. Practice exercises
4. Mock interview scenarios
5. Progress milestones

Prioritize the most critical gaps first.

Return as JSON with structure:
{{
  "week_1": [
    {{"day": 1, "activity": "...", "duration": "...", "resources": [...]}}
  ],
  "week_2": [...],
  "milestones": [...]
}}
"""
        
        response = self._generate_response(plan_prompt, response_format="json")
        return json.loads(response)
    
    def _benchmark_performance(
        self,
        aggregate_metrics: Dict[str, Any],
        role: str,
    ) -> Dict[str, Any]:
        """Tool: Benchmark performance against role expectations.
        
        Args:
            aggregate_metrics: Aggregate performance metrics
            role: Target role
            
        Returns:
            Benchmark comparison
        """
        benchmark_prompt = f"""
Target Role: {role}

Candidate Performance:
{json.dumps(aggregate_metrics, indent=2)}

Compare to typical performance expectations for this role:
1. Where do they stand? (bottom 25% / middle 50% / top 25%)
2. Which dimensions are above/below expectations?
3. What's their readiness level? (not ready / needs work / ready / strong)
4. How many more practice sessions recommended?

Return as JSON.
"""
        
        response = self._generate_response(benchmark_prompt, response_format="json")
        return json.loads(response)
    
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive coaching report.
        
        Args:
            context: Contains full session data (strategy, history, evaluations, etc.)
            
        Returns:
            Coaching report in Markdown format
        """
        role = context.get("candidate_role", "")
        focus_area = context.get("focus_area", "")
        strategy = context.get("strategy", {})
        history = context.get("conversation_history", [])
        evaluations = context.get("turn_scores", [])
        aggregate_metrics = context.get("aggregate_metrics", {})
        
        # Store in working memory
        self.update_memory("role", role)
        self.update_memory("focus_area", focus_area)
        
        # Use tools to analyze
        skill_gaps = self._identify_skill_gaps(evaluations, role)
        self.update_memory("skill_gaps", skill_gaps)
        
        practice_plan = self._generate_practice_plan(skill_gaps, role, focus_area)
        self.update_memory("practice_plan", practice_plan)
        
        benchmark = self._benchmark_performance(aggregate_metrics, role)
        self.update_memory("benchmark", benchmark)
        
        # Generate comprehensive report
        report_prompt = f"""
Complete Session Data:

Candidate Role: {role}
Focus Area: {focus_area}

Session Strategy:
{json.dumps(strategy, indent=2)}

Conversation History:
{json.dumps(history, indent=2)}

Turn Scores:
{json.dumps(evaluations, indent=2)}

Aggregate Metrics:
{json.dumps(aggregate_metrics, indent=2)}

Skill Gaps Analysis:
{json.dumps(skill_gaps, indent=2)}

Performance Benchmark:
{json.dumps(benchmark, indent=2)}

Practice Plan:
{json.dumps(practice_plan, indent=2)}

Generate your comprehensive coaching report in Markdown format following the structure in your system prompt.
Include all the analysis above in an actionable, encouraging format.
"""
        
        report = self._generate_response(report_prompt, temperature=0.7)
        
        # Store in long-term memory
        self.update_memory("coaching_report", report, "long_term")
        self.update_memory("session_completed", {
            "role": role,
            "total_turns": len(history),
            "avg_score": aggregate_metrics.get("avg_completeness", 0),
        }, "short_term")
        
        return {
            "report": report,
            "skill_gaps": skill_gaps,
            "practice_plan": practice_plan,
            "benchmark": benchmark,
            "agent": self.config.name,
        }
    
    def generate_comparison_report(
        self,
        previous_sessions: List[Dict[str, Any]],
    ) -> str:
        """Generate a comparison report across multiple sessions.
        
        This enables tracking progress over time.
        
        Args:
            previous_sessions: List of previous session data
            
        Returns:
            Comparison report in Markdown
        """
        comparison_prompt = f"""
Previous Sessions:
{json.dumps(previous_sessions, indent=2)}

Current Session:
{json.dumps(self.memory.long_term, indent=2)}

Generate a progress comparison report showing:
1. Performance trends across sessions
2. Skill gaps that were closed
3. New areas of improvement
4. Overall trajectory
5. Adjusted recommendations

Return as Markdown.
"""
        
        comparison_report = self._generate_response(comparison_prompt, temperature=0.7)
        self.update_memory("comparison_report", comparison_report, "long_term")
        
        return comparison_report
