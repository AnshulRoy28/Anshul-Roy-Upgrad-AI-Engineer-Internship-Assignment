"""Interviewer agent - conducts the interview."""
import config


def get_interviewer_prompt() -> str:
    """Get the Interviewer agent prompt."""
    prompt = config.load_prompt("interviewer.md")
    
    full_prompt = f"""{prompt}

## Session Context

You have access to:
- session_strategy: The interview strategy created by the Profiler
- last_evaluator_signal: The signal from the previous turn (if any)
- current_turn: The current turn number
- conversation_history: All previous questions and answers

Use the session_strategy to guide your questions.
Use the last_evaluator_signal to determine your next move.

Generate ONLY the question text you want to ask. Do not include any preamble or explanation.
"""
    
    return full_prompt
