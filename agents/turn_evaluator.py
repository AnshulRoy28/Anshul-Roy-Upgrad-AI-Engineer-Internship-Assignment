"""Turn Evaluator agent - scores each answer."""
import config


def get_turn_evaluator_prompt() -> str:
    """Get the Turn Evaluator agent prompt."""
    prompt = config.load_prompt("turn_evaluator.md")
    
    full_prompt = f"""{prompt}

## Session Context

You have access to:
- session_strategy: The interview strategy (for role/seniority context)
- conversation_history: All questions and answers so far
- current_turn: The current turn number

Your job is to evaluate the MOST RECENT answer in the conversation history.

Output your evaluation as a JSON object following the schema defined above.
"""
    
    return full_prompt
