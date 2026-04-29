# Configuration constants for the AI Mock Interview Coach

import os
from pathlib import Path

MODEL = "gemini-2.0-flash"
MAX_INTERVIEW_TURNS = 7
APP_NAME = "interview-coach"

# Get the base directory
BASE_DIR = Path(__file__).parent


def load_prompt(filename: str) -> str:
    """Load a prompt file from the prompts directory."""
    prompt_path = BASE_DIR / "prompts" / filename
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()
