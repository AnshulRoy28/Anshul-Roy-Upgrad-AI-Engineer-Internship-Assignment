# Coach Agent - provides final feedback report

from google.adk.agents import LlmAgent
from config import MODEL, load_prompt
from state import schema

# Load the coach prompt
COACH_PROMPT = load_prompt("coach.md")

# Create the Coach agent
coach_agent = LlmAgent(
    name="Coach",
    model=MODEL,
    instruction=COACH_PROMPT,
    description="Synthesizes interview performance into actionable coaching feedback",
    output_key=schema.COACHING_REPORT,
    include_contents='none'  # Reads from state, not conversation history
)
