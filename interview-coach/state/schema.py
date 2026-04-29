# State schema - defines all state keys used across agents

# Input keys (set by main.py before pipeline starts)
CANDIDATE_ROLE = "candidate_role"
CANDIDATE_BACKGROUND = "candidate_background"
FOCUS_AREA = "focus_area"

# Profiler output
SESSION_STRATEGY = "session_strategy"

# Interview loop state
CONVERSATION_HISTORY = "conversation_history"
TURN_SCORES = "turn_scores"
LAST_EVALUATOR_SIGNAL = "last_evaluator_signal"
CURRENT_TURN = "current_turn"
INTERVIEW_COMPLETE = "interview_complete"

# Coach output
COACHING_REPORT = "coaching_report"


# Helper functions
def append_turn_score(state: dict, score: dict) -> None:
    """Append a turn score to the turn_scores list in state."""
    if TURN_SCORES not in state:
        state[TURN_SCORES] = []
    state[TURN_SCORES].append(score)


def get_last_signal(state: dict) -> str:
    """Get the last evaluator signal from state."""
    return state.get(LAST_EVALUATOR_SIGNAL, "advance")


def increment_turn(state: dict) -> None:
    """Increment the current turn counter."""
    state[CURRENT_TURN] = state.get(CURRENT_TURN, 0) + 1


def mark_interview_complete(state: dict) -> None:
    """Mark the interview as complete."""
    state[INTERVIEW_COMPLETE] = True


def is_interview_complete(state: dict) -> bool:
    """Check if the interview is complete."""
    return state.get(INTERVIEW_COMPLETE, False)
