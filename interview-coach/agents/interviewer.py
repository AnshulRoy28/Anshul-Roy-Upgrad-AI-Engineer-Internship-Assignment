# Interviewer Agent - conducts the live interview

from google.adk.agents import LlmAgent
from config import MODEL, load_prompt
from tools.cli_input import get_candidate_response

# Load the interviewer prompt
INTERVIEWER_PROMPT = load_prompt("interviewer.md")

# Create the Interviewer agent
interviewer_agent = LlmAgent(
    name="Interviewer",
    model=MODEL,
    instruction=INTERVIEWER_PROMPT,
    description="Conducts the mock interview by asking questions and following up",
    tools=[get_candidate_response]
)
