"""Agent definitions for the interview coach."""
from agents.profiler import get_profiler_prompt
from agents.interviewer import get_interviewer_prompt
from agents.turn_evaluator import get_turn_evaluator_prompt
from agents.coach import get_coach_prompt

__all__ = [
    "get_profiler_prompt",
    "get_interviewer_prompt",
    "get_turn_evaluator_prompt",
    "get_coach_prompt",
]
