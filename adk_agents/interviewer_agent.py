"""Interviewer Agent - Conducts the interview using ADK patterns."""
import json
from typing import Any, Dict, List
from adk_agents.base_agent import BaseInterviewAgent, AgentConfig
from google.genai import Client
import config


class InterviewerAgent(BaseInterviewAgent):
    """Agent that conducts the interview conversation."""
    
    def __init__(self, client: Client):
        """Initialize the Interviewer agent."""
        agent_config = AgentConfig(
            name="Interviewer",
            role="Conversational Agent - Asks questions and maintains interview flow",
            temperature=0.8,
            response_format="text",
            max_iterations=1,
        )
        
        system_prompt = config.load_prompt("interviewer.md")
        super().__init__(client, agent_config, system_prompt)
        
        # Register tools
        self.register_tool(
            "generate_followup",
            self._generate_followup,
            "Generates a follow-up question based on previous answer"
        )
        
        self.register_tool(
            "select_next_competency",
            self._select_next_competency,
            "Selects the next competency area to explore"
        )
    
    def _generate_followup(self, answer: str, question: str) -> str:
        """Tool: Generate a follow-up question.
        
        Args:
            answer: Candidate's previous answer
            question: Previous question asked
            
        Returns:
            Follow-up question
        """
        followup_prompt = f"""
Previous Question: {question}
Candidate's Answer: {answer}

Generate a natural follow-up question that:
1. Digs deeper into their answer
2. Clarifies vague points
3. Explores related scenarios

Return ONLY the follow-up question text.
"""
        
        return self._generate_response(followup_prompt, temperature=0.9)
    
    def _select_next_competency(
        self,
        strategy: Dict[str, Any],
        covered_competencies: List[str],
        turn_number: int,
    ) -> str:
        """Tool: Select the next competency to assess.
        
        Args:
            strategy: Interview strategy
            covered_competencies: Already covered competencies
            turn_number: Current turn number
            
        Returns:
            Next competency to explore
        """
        selection_prompt = f"""
Interview Strategy:
{json.dumps(strategy, indent=2)}

Already Covered: {covered_competencies}
Current Turn: {turn_number}

Based on the difficulty arc and competency pillars, which competency should we explore next?

Return ONLY the competency name.
"""
        
        return self._generate_response(selection_prompt, temperature=0.5).strip()
    
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the next interview question.
        
        Args:
            context: Contains strategy, last_signal, conversation_history, turn_number
            
        Returns:
            Next question to ask
        """
        strategy = context.get("strategy", {})
        last_signal = context.get("last_signal", "advance")
        history = context.get("conversation_history", [])
        turn_number = context.get("turn_number", 1)
        
        # Store in working memory
        self.update_memory("current_turn", turn_number)
        self.update_memory("last_signal", last_signal)
        
        # Determine covered competencies
        covered_competencies = self.get_memory("covered_competencies", "working") or []
        
        # Handle different signals
        if last_signal == "probe_deeper" and history:
            # Generate follow-up question
            last_qa = history[-1]
            question = self._generate_followup(
                last_qa.get("answer", ""),
                last_qa.get("question", "")
            )
            
            self.update_memory("question_type", "followup", "short_term")
        
        elif last_signal == "clarify" and history:
            # Ask for clarification
            last_qa = history[-1]
            clarification_prompt = f"""
The candidate's last answer was unclear or off-topic:
Question: {last_qa.get('question', '')}
Answer: {last_qa.get('answer', '')}

Generate a polite clarification question that redirects them back on track.
Return ONLY the question text.
"""
            question = self._generate_response(clarification_prompt, temperature=0.7)
            self.update_memory("question_type", "clarification", "short_term")
        
        else:
            # Select next competency and generate new question
            next_competency = self._select_next_competency(
                strategy,
                covered_competencies,
                turn_number
            )
            
            covered_competencies.append(next_competency)
            self.update_memory("covered_competencies", covered_competencies)
            
            # Generate question for this competency
            question_prompt = f"""
Session Strategy:
{json.dumps(strategy, indent=2)}

Current Turn: {turn_number}
Target Competency: {next_competency}
Last Signal: {last_signal}

Conversation History:
{json.dumps(history, indent=2)}

Generate your next question following the strategy and difficulty arc.
Return ONLY the question text.
"""
            
            question = self._generate_response(question_prompt, temperature=0.8)
            self.update_memory("question_type", "new_competency", "short_term")
            self.update_memory("current_competency", next_competency)
        
        # Store question in memory
        self.update_memory("last_question", question, "short_term")
        
        return {
            "question": question.strip(),
            "turn_number": turn_number,
            "signal_handled": last_signal,
            "agent": self.config.name,
        }
    
    def adjust_tone(self, feedback: Dict[str, Any]) -> None:
        """Adjust interviewer tone based on feedback.
        
        This enables adaptive interviewing style.
        
        Args:
            feedback: Feedback about interview tone/style
        """
        adjustment_prompt = f"""
Feedback on your interviewing style:
{json.dumps(feedback, indent=2)}

How should you adjust your tone, pacing, or question style?
Provide specific adjustments.
"""
        
        adjustments = self._generate_response(adjustment_prompt, temperature=0.6)
        self.update_memory("tone_adjustments", adjustments, "long_term")
        self.update_memory("tone_feedback", feedback, "short_term")
