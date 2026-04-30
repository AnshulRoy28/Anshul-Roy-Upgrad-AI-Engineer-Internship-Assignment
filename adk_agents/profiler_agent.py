"""Profiler Agent - Creates interview strategy using ADK patterns."""
import json
from typing import Any, Dict
from adk_agents.base_agent import BaseInterviewAgent, AgentConfig
from google.genai import Client
import config


class ProfilerAgent(BaseInterviewAgent):
    """Agent that analyzes candidate profile and creates interview strategy."""
    
    def __init__(self, client: Client):
        """Initialize the Profiler agent."""
        agent_config = AgentConfig(
            name="Profiler",
            role="Strategic Planner - Analyzes candidate and creates interview strategy",
            temperature=0.7,
            response_format="json",
            max_iterations=1,
        )
        
        system_prompt = config.load_prompt("profiler.md")
        super().__init__(client, agent_config, system_prompt)
        
        # Register tools
        self.register_tool(
            "analyze_role_complexity",
            self._analyze_role_complexity,
            "Analyzes the complexity and seniority level of a role"
        )
    
    def _analyze_role_complexity(self, role: str) -> Dict[str, Any]:
        """Tool: Analyze role complexity and seniority.
        
        Args:
            role: The target role
            
        Returns:
            Analysis of role complexity
        """
        analysis_prompt = f"""
Analyze this role for interview planning:
Role: {role}

Provide:
1. Seniority level (entry/mid/senior/executive)
2. Key competency areas (3-5 areas)
3. Typical interview difficulty
4. Critical skills to assess

Return as JSON.
"""
        
        response = self._generate_response(analysis_prompt, response_format="json")
        return json.loads(response)
    
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process candidate information and create interview strategy.
        
        Args:
            context: Contains candidate_role, candidate_background, focus_area
            
        Returns:
            Interview strategy as JSON
        """
        # Store context in working memory
        self.update_memory("candidate_role", context.get("candidate_role"))
        self.update_memory("candidate_background", context.get("candidate_background"))
        self.update_memory("focus_area", context.get("focus_area"))
        
        # Use tool to analyze role complexity
        role_analysis = self._analyze_role_complexity(context.get("candidate_role"))
        self.update_memory("role_analysis", role_analysis)
        
        # Build strategy generation prompt
        strategy_prompt = f"""
Candidate Information:
- Role: {context.get('candidate_role')}
- Background: {context.get('candidate_background')}
- Focus Area: {context.get('focus_area')}

Role Analysis:
{json.dumps(role_analysis, indent=2)}

Create a comprehensive interview strategy JSON following the schema in your system prompt.
"""
        
        # Generate strategy
        strategy_json = self._generate_response(strategy_prompt, response_format="json")
        strategy = json.loads(strategy_json)
        
        # Store in long-term memory
        self.update_memory("strategy", strategy, "long_term")
        
        # Add to short-term memory for tracking
        self.update_memory("strategy_created", {
            "role": context.get("candidate_role"),
            "timestamp": "now",
            "competencies": len(strategy.get("competency_pillars", [])),
        }, "short_term")
        
        return {
            "strategy": strategy,
            "role_analysis": role_analysis,
            "agent": self.config.name,
        }
    
    def adapt_strategy(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt the strategy based on interview progress.
        
        This enables dynamic strategy adjustment during the interview.
        
        Args:
            feedback: Feedback from evaluator or interviewer
            
        Returns:
            Updated strategy
        """
        current_strategy = self.get_memory("strategy", "long_term")
        
        adaptation_prompt = f"""
Current Strategy:
{json.dumps(current_strategy, indent=2)}

Feedback from Interview:
{json.dumps(feedback, indent=2)}

Adapt the strategy to better match the candidate's performance level.
Adjust difficulty, focus areas, or competency emphasis as needed.

Return the updated strategy JSON.
"""
        
        updated_strategy_json = self._generate_response(adaptation_prompt, response_format="json")
        updated_strategy = json.loads(updated_strategy_json)
        
        self.update_memory("strategy", updated_strategy, "long_term")
        self.update_memory("strategy_adapted", feedback, "short_term")
        
        return {
            "updated_strategy": updated_strategy,
            "adaptation_reason": feedback,
        }
