# Interview Loop - orchestrates the Interviewer and Turn Evaluator

from google.adk.agents import LoopAgent
from config import MAX_INTERVIEW_TURNS
from agents.interviewer import interviewer_agent
from agents.turn_evaluator import turn_evaluator_agent
from state import schema


def should_continue_loop(state: dict) -> bool:
    """
    Termination condition for the loop.
    Returns False if interview is complete, True otherwise.
    """
    return not schema.is_interview_complete(state)


# Create the Interview Loop
interview_loop = LoopAgent(
    name="InterviewLoop",
    sub_agents=[interviewer_agent, turn_evaluator_agent],
    max_iterations=MAX_INTERVIEW_TURNS,
    description="Conducts interview turns until completion"
)
