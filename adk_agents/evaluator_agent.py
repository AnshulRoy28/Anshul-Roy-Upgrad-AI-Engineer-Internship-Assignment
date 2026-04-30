"""Evaluator Agent - Scores answers using ADK patterns."""
import json
from typing import Any, Dict, List
from adk_agents.base_agent import BaseInterviewAgent, AgentConfig
from google.genai import Client
import config


class EvaluatorAgent(BaseInterviewAgent):
    """Agent that evaluates candidate answers and provides signals."""
    
    def __init__(self, client: Client):
        """Initialize the Evaluator agent."""
        agent_config = AgentConfig(
            name="TurnEvaluator",
            role="Silent Judge - Scores answers and emits signals",
            temperature=0.3,
            response_format="json",
            max_iterations=1,
        )
        
        system_prompt = config.load_prompt("turn_evaluator.md")
        super().__init__(client, agent_config, system_prompt)
        
        # Register tools
        self.register_tool(
            "detect_answer_patterns",
            self._detect_answer_patterns,
            "Detects patterns in candidate's answering style"
        )
        
        self.register_tool(
            "compare_to_baseline",
            self._compare_to_baseline,
            "Compares answer quality to expected baseline for role"
        )
    
    def _detect_answer_patterns(self, answers: List[str]) -> Dict[str, Any]:
        """Tool: Detect patterns in answering style.
        
        Args:
            answers: List of candidate answers
            
        Returns:
            Detected patterns
        """
        pattern_prompt = f"""
Analyze these answers for patterns:
{json.dumps(answers, indent=2)}

Detect:
1. Consistent strengths (e.g., always uses STAR format)
2. Consistent weaknesses (e.g., always vague on metrics)
3. Answer length trends
4. Confidence level trends
5. Technical depth trends

Return as JSON.
"""
        
        response = self._generate_response(pattern_prompt, response_format="json")
        return json.loads(response)
    
    def _compare_to_baseline(
        self,
        answer: str,
        role: str,
        competency: str,
    ) -> Dict[str, Any]:
        """Tool: Compare answer to expected baseline.
        
        Args:
            answer: Candidate's answer
            role: Target role
            competency: Competency being assessed
            
        Returns:
            Comparison to baseline
        """
        comparison_prompt = f"""
Role: {role}
Competency: {competency}
Answer: {answer}

Compare this answer to what you'd expect from a qualified candidate for this role.

Provide:
1. Expected baseline quality (1-5)
2. Actual quality (1-5)
3. Gap analysis
4. Key missing elements

Return as JSON.
"""
        
        response = self._generate_response(comparison_prompt, response_format="json")
        return json.loads(response)
    
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the candidate's answer.
        
        Args:
            context: Contains question, answer, strategy, turn_number, history
            
        Returns:
            Evaluation scores and next-move signal
        """
        question = context.get("question", "")
        answer = context.get("answer", "")
        strategy = context.get("strategy", {})
        turn_number = context.get("turn_number", 1)
        history = context.get("conversation_history", [])
        
        # Store in working memory
        self.update_memory("current_turn", turn_number)
        self.update_memory("current_answer", answer)
        
        # Detect patterns if we have enough history
        if len(history) >= 2:
            all_answers = [qa.get("answer", "") for qa in history]
            patterns = self._detect_answer_patterns(all_answers)
            self.update_memory("answer_patterns", patterns)
        else:
            patterns = {}
        
        # Compare to baseline
        role = strategy.get("role", "")
        current_competency = context.get("current_competency", "general")
        baseline_comparison = self._compare_to_baseline(answer, role, current_competency)
        self.update_memory("baseline_comparison", baseline_comparison)
        
        # Build evaluation prompt
        eval_prompt = f"""
Session Strategy:
{json.dumps(strategy, indent=2)}

Current Turn: {turn_number}

Question Asked: {question}

Candidate's Answer: {answer}

Detected Patterns:
{json.dumps(patterns, indent=2)}

Baseline Comparison:
{json.dumps(baseline_comparison, indent=2)}

Evaluate this answer and provide your JSON assessment following the schema in your system prompt.
"""
        
        # Generate evaluation
        evaluation_json = self._generate_response(eval_prompt, response_format="json")
        evaluation = json.loads(evaluation_json)
        evaluation["turn"] = turn_number
        
        # Store in memory
        self.update_memory(f"evaluation_turn_{turn_number}", evaluation, "long_term")
        self.update_memory("last_evaluation", evaluation, "short_term")
        
        # Calculate aggregate metrics
        all_evaluations = [
            self.get_memory(f"evaluation_turn_{i}", "long_term")
            for i in range(1, turn_number + 1)
            if self.get_memory(f"evaluation_turn_{i}", "long_term")
        ]
        
        aggregate_metrics = self._calculate_aggregate_metrics(all_evaluations)
        self.update_memory("aggregate_metrics", aggregate_metrics)
        
        return {
            "evaluation": evaluation,
            "patterns": patterns,
            "baseline_comparison": baseline_comparison,
            "aggregate_metrics": aggregate_metrics,
            "agent": self.config.name,
        }
    
    def _calculate_aggregate_metrics(
        self,
        evaluations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Calculate aggregate metrics across all evaluations.
        
        Args:
            evaluations: List of all evaluations
            
        Returns:
            Aggregate metrics
        """
        if not evaluations:
            return {}
        
        # Calculate averages
        dimensions = ["completeness", "depth", "structure", "relevance", "confidence"]
        averages = {}
        
        for dim in dimensions:
            scores = [
                e.get("scores", {}).get(dim, 0)
                for e in evaluations
                if e and e.get("scores")
            ]
            if scores:
                averages[f"avg_{dim}"] = sum(scores) / len(scores)
        
        # Calculate trends
        if len(evaluations) >= 3:
            recent_avg = sum(
                e.get("scores", {}).get("completeness", 0)
                for e in evaluations[-3:]
            ) / 3
            
            early_avg = sum(
                e.get("scores", {}).get("completeness", 0)
                for e in evaluations[:3]
            ) / 3
            
            averages["trend"] = "improving" if recent_avg > early_avg else "declining"
        
        return averages
    
    def predict_final_outcome(self) -> Dict[str, Any]:
        """Predict likely final interview outcome based on current performance.
        
        This enables proactive coaching and strategy adjustment.
        
        Returns:
            Predicted outcome and confidence
        """
        aggregate = self.get_memory("aggregate_metrics", "working") or {}
        patterns = self.get_memory("answer_patterns", "working") or {}
        
        prediction_prompt = f"""
Current Performance Metrics:
{json.dumps(aggregate, indent=2)}

Detected Patterns:
{json.dumps(patterns, indent=2)}

Based on this data, predict:
1. Likely final interview outcome (strong pass / pass / borderline / fail)
2. Confidence in prediction (0-100%)
3. Key factors influencing prediction
4. What could change the outcome

Return as JSON.
"""
        
        prediction_json = self._generate_response(prediction_prompt, response_format="json")
        prediction = json.loads(prediction_json)
        
        self.update_memory("outcome_prediction", prediction, "long_term")
        
        return prediction
