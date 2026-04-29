# Profiler Agent - transforms candidate input into interview strategy

from google.adk.agents import LlmAgent
from config import MODEL, load_prompt
from state import schema

# Load the profiler prompt
PROFILER_PROMPT = load_prompt("profiler.md")

# Create the Profiler agent
profiler_agent = LlmAgent(
    name="Profiler",
    model=MODEL,
    instruction=PROFILER_PROMPT,
    description="Transforms candidate input into a structured interview strategy",
    output_key=schema.SESSION_STRATEGY,
    include_contents='none'  # Stateless - only uses current input
)
