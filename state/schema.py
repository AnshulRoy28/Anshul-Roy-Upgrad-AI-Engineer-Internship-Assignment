"""Session state schema and helper functions."""
from typing import Any, Dict, List

# State key constants
CANDIDATE_ROLE = "candidate_role"
CANDIDATE_BACKGROUND = "candidate_background"
FOCUS_AREA = "focus_area"
SESSION_STRATEGY = "session_strategy"
CONVERSATION_HISTORY = "conversation_history"
TURN_SCORES = "turn_scores"
LAST_EVALUATOR_SIGNAL = "last_evaluator_signal"
CURRENT_TURN = "current_turn"
INTERVIEW_COMPLETE = "interview_complete"
COACHING_REPORT = "coaching_report"


def initialize_state(role: str, background: str, focus_area: str) -> Dict[str, Any]:
    """Initialize session state with candidate inputs."""
    return {
        CANDIDATE_ROLE: role,
        CANDIDATE_BACKGROUND: background,
        FOCUS_AREA: focus_area,
        CURRENT_TURN: 0,
        INTERVIEW_COMPLETE: False,
        CONVERSATION_HISTORY: [],
        TURN_SCORES: [],
    }


def append_turn_score(state: Dict[str, Any], score: Dict[str, Any]) -> None:
    """Append a turn score to the session state."""
    if TURN_SCORES not in state:
        state[TURN_SCORES] = []
    state[TURN_SCORES].append(score)


def get_last_signal(state: Dict[str, Any]) -> str:
    """Get the last evaluator signal from state."""
    return state.get(LAST_EVALUATOR_SIGNAL, "advance")


def increment_turn(state: Dict[str, Any]) -> None:
    """Increment the current turn counter."""
    state[CURRENT_TURN] = state.get(CURRENT_TURN, 0) + 1


def mark_interview_complete(state: Dict[str, Any]) -> None:
    """Mark the interview as complete."""
    state[INTERVIEW_COMPLETE] = True


def is_interview_complete(state: Dict[str, Any]) -> bool:
    """Check if the interview is complete."""
    return state.get(INTERVIEW_COMPLETE, False)


def add_conversation_turn(
    state: Dict[str, Any], question: str, answer: str
) -> None:
    """Add a question-answer pair to conversation history."""
    if CONVERSATION_HISTORY not in state:
        state[CONVERSATION_HISTORY] = []
    state[CONVERSATION_HISTORY].append({"question": question, "answer": answer})
