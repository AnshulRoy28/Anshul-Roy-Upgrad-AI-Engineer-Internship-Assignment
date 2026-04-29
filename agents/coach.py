"""Coach agent - provides final feedback."""
import config


def get_coach_prompt() -> str:
    """Get the Coach agent prompt."""
    prompt = config.load_prompt("coach.md")
    
    full_prompt = f"""{prompt}

## Session Context

You have access to the complete session state:
- session_strategy: The interview strategy
- conversation_history: Full transcript of all questions and answers
- turn_scores: All evaluator scores for each turn
- candidate_role: The target role
- focus_area: The interview focus

Analyze all of this information and produce your coaching report in Markdown format.
"""
    
    return full_prompt
