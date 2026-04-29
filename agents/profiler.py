"""Profiler agent - creates interview strategy."""
import config


def get_profiler_prompt() -> str:
    """Get the Profiler agent prompt."""
    prompt = config.load_prompt("profiler.md")
    
    full_prompt = f"""{prompt}

## Current Candidate Information

You will receive the following information from the session state:
- candidate_role: The target role
- candidate_background: Background information (may be empty)
- focus_area: The interview focus area

Analyze this information and produce your strategy JSON.
"""
    
    return full_prompt
