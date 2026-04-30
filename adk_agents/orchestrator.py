"""Multi-Agent Orchestrator using ADK patterns."""
import asyncio
import json
from typing import Any, Dict, List, Optional
from google.genai import Client
from adk_agents.profiler_agent import ProfilerAgent
from adk_agents.interviewer_agent import InterviewerAgent
from adk_agents.evaluator_agent import EvaluatorAgent
from adk_agents.coach_agent import CoachAgent
import state
import config


class InterviewOrchestrator:
    """Orchestrates the multi-agent interview system."""
    
    def __init__(self, client: Client):
        """Initialize the orchestrator with all agents.
        
        Args:
            client: Google GenAI client
        """
        self.client = client
        
        # Initialize all agents
        self.profiler = ProfilerAgent(client)
        self.interviewer = InterviewerAgent(client)
        self.evaluator = EvaluatorAgent(client)
        self.coach = CoachAgent(client)
        
        # Session state
        self.session_state: Optional[Dict[str, Any]] = None
        
        # Orchestration metadata
        self.metadata = {
            "total_agent_calls": 0,
            "agent_call_log": [],
            "errors": [],
        }
    
    def initialize_session(
        self,
        role: str,
        background: str,
        focus_area: str,
    ) -> Dict[str, Any]:
        """Initialize a new interview session.
        
        Args:
            role: Target role
            background: Candidate background
            focus_area: Interview focus area
            
        Returns:
            Initialized session state
        """
        self.session_state = state.initialize_state(role, background, focus_area)
        
        # Log initialization
        self.metadata["agent_call_log"].append({
            "action": "session_initialized",
            "role": role,
            "focus_area": focus_area,
        })
        
        return self.session_state
    
    def run_profiler_phase(self) -> Dict[str, Any]:
        """Run the profiler phase to create interview strategy.
        
        Returns:
            Strategy and analysis
        """
        print("\n🔍 Profiler Agent: Analyzing profile and creating strategy...")
        
        context = {
            "candidate_role": self.session_state[state.CANDIDATE_ROLE],
            "candidate_background": self.session_state[state.CANDIDATE_BACKGROUND],
            "focus_area": self.session_state[state.FOCUS_AREA],
        }
        
        result = self.profiler.process(context)
        
        # Store strategy in session state
        self.session_state[state.SESSION_STRATEGY] = result["strategy"]
        
        # Log agent call
        self.metadata["total_agent_calls"] += 1
        self.metadata["agent_call_log"].append({
            "agent": "Profiler",
            "action": "create_strategy",
            "result_keys": list(result.keys()),
        })
        
        print("✅ Strategy created!")
        return result
    
    def run_interview_turn(self, turn_number: int) -> bool:
        """Run a single interview turn.
        
        Args:
            turn_number: Current turn number
            
        Returns:
            True if interview should continue, False otherwise
        """
        # Interviewer generates question
        interviewer_context = {
            "strategy": self.session_state[state.SESSION_STRATEGY],
            "last_signal": self.session_state.get(state.LAST_EVALUATOR_SIGNAL, "advance"),
            "conversation_history": self.session_state[state.CONVERSATION_HISTORY],
            "turn_number": turn_number,
            "current_competency": self.interviewer.get_memory("current_competency", "working"),
        }
        
        interviewer_result = self.interviewer.process(interviewer_context)
        question = interviewer_result["question"]
        
        self.metadata["total_agent_calls"] += 1
        self.metadata["agent_call_log"].append({
            "agent": "Interviewer",
            "turn": turn_number,
            "action": "generate_question",
        })
        
        # Present question and get answer
        print(f"\n🎤 Interviewer: {question}\n")
        print("💭 You: ", end="", flush=True)
        answer = input().strip()
        
        while not answer:
            print("💭 You: ", end="", flush=True)
            answer = input().strip()
        
        # Record conversation
        state.add_conversation_turn(self.session_state, question, answer)
        
        # Evaluator scores the answer
        evaluator_context = {
            "question": question,
            "answer": answer,
            "strategy": self.session_state[state.SESSION_STRATEGY],
            "turn_number": turn_number,
            "conversation_history": self.session_state[state.CONVERSATION_HISTORY],
            "current_competency": self.interviewer.get_memory("current_competency", "working"),
        }
        
        evaluator_result = self.evaluator.process(evaluator_context)
        evaluation = evaluator_result["evaluation"]
        
        self.metadata["total_agent_calls"] += 1
        self.metadata["agent_call_log"].append({
            "agent": "Evaluator",
            "turn": turn_number,
            "action": "evaluate_answer",
            "next_move": evaluation.get("next_move"),
        })
        
        # Store evaluation
        state.append_turn_score(self.session_state, evaluation)
        self.session_state[state.LAST_EVALUATOR_SIGNAL] = evaluation["next_move"]
        self.session_state["aggregate_metrics"] = evaluator_result.get("aggregate_metrics", {})
        
        # Check if interview should end
        if evaluation["next_move"] == "wrap_up" or turn_number >= config.MAX_INTERVIEW_TURNS:
            return False
        
        return True
    
    def run_coach_phase(self) -> Dict[str, Any]:
        """Run the coach phase to generate final feedback.
        
        Returns:
            Coaching report and analysis
        """
        print("\n📊 Coach Agent: Analyzing performance and generating feedback...")
        
        context = {
            "candidate_role": self.session_state[state.CANDIDATE_ROLE],
            "focus_area": self.session_state[state.FOCUS_AREA],
            "strategy": self.session_state[state.SESSION_STRATEGY],
            "conversation_history": self.session_state[state.CONVERSATION_HISTORY],
            "turn_scores": self.session_state[state.TURN_SCORES],
            "aggregate_metrics": self.session_state.get("aggregate_metrics", {}),
        }
        
        result = self.coach.process(context)
        
        # Store report in session state
        self.session_state[state.COACHING_REPORT] = result["report"]
        
        # Log agent call
        self.metadata["total_agent_calls"] += 1
        self.metadata["agent_call_log"].append({
            "agent": "Coach",
            "action": "generate_report",
            "result_keys": list(result.keys()),
        })
        
        print("✅ Coaching report generated!")
        return result
    
    def run_full_interview(
        self,
        role: str,
        background: str,
        focus_area: str,
    ) -> Dict[str, Any]:
        """Run a complete interview session.
        
        Args:
            role: Target role
            background: Candidate background
            focus_area: Interview focus area
            
        Returns:
            Complete session results
        """
        # Initialize session
        self.initialize_session(role, background, focus_area)
        
        # Run profiler
        profiler_result = self.run_profiler_phase()
        
        # Run interview loop
        print("\n" + "=" * 60)
        print("🎬 Let's begin the interview!")
        print("=" * 60)
        
        turn = 1
        while turn <= config.MAX_INTERVIEW_TURNS:
            should_continue = self.run_interview_turn(turn)
            state.increment_turn(self.session_state)
            turn += 1
            
            if not should_continue:
                break
        
        # Run coach
        print("\n" + "=" * 60)
        print("🎓 Interview Complete!")
        print("=" * 60)
        
        coach_result = self.run_coach_phase()
        
        return {
            "session_state": self.session_state,
            "profiler_result": profiler_result,
            "coach_result": coach_result,
            "metadata": self.metadata,
        }
    
    def enable_adaptive_strategy(self) -> None:
        """Enable adaptive strategy adjustment during interview.
        
        This allows the profiler to adjust strategy based on performance.
        """
        # Check if adaptation is needed after turn 3
        if self.session_state[state.CURRENT_TURN] >= 3:
            aggregate = self.session_state.get("aggregate_metrics", {})
            
            # If performance is significantly off from expected
            avg_score = aggregate.get("avg_completeness", 3.0)
            
            if avg_score < 2.5 or avg_score > 4.5:
                print("\n🔄 Adapting interview strategy based on performance...")
                
                feedback = {
                    "current_performance": aggregate,
                    "adjustment_reason": "Performance significantly different from expected",
                }
                
                adaptation_result = self.profiler.adapt_strategy(feedback)
                self.session_state[state.SESSION_STRATEGY] = adaptation_result["updated_strategy"]
                
                self.metadata["agent_call_log"].append({
                    "agent": "Profiler",
                    "action": "adapt_strategy",
                    "reason": feedback["adjustment_reason"],
                })
                
                print("✅ Strategy adapted!")
    
    def enable_outcome_prediction(self) -> Dict[str, Any]:
        """Enable outcome prediction during interview.
        
        Returns:
            Predicted outcome
        """
        if self.session_state[state.CURRENT_TURN] >= 3:
            print("\n🔮 Predicting likely interview outcome...")
            
            prediction = self.evaluator.predict_final_outcome()
            
            self.metadata["agent_call_log"].append({
                "agent": "Evaluator",
                "action": "predict_outcome",
                "prediction": prediction.get("outcome"),
            })
            
            return prediction
        
        return {}
    
    def get_agent_insights(self) -> Dict[str, Any]:
        """Get insights from all agents' memories.
        
        Returns:
            Aggregated insights from all agents
        """
        return {
            "profiler": {
                "strategy": self.profiler.get_memory("strategy", "long_term"),
                "role_analysis": self.profiler.get_memory("role_analysis", "working"),
            },
            "interviewer": {
                "covered_competencies": self.interviewer.get_memory("covered_competencies", "working"),
                "tone_adjustments": self.interviewer.get_memory("tone_adjustments", "long_term"),
            },
            "evaluator": {
                "aggregate_metrics": self.evaluator.get_memory("aggregate_metrics", "working"),
                "answer_patterns": self.evaluator.get_memory("answer_patterns", "working"),
            },
            "coach": {
                "skill_gaps": self.coach.get_memory("skill_gaps", "working"),
                "benchmark": self.coach.get_memory("benchmark", "working"),
            },
        }
