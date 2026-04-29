# Full Interview Pipeline - orchestrates all agents

from google.adk.agents import SequentialAgent
from agents.profiler import profiler_agent
from agents.coach import coach_agent
from orchestration.interview_loop import interview_loop

# Create the full pipeline
interview_pipeline = SequentialAgent(
    name="InterviewPipeline",
    sub_agents=[
        profiler_agent,
        interview_loop,
        coach_agent
    ],
    description="Complete interview pipeline: strategy → interview → coaching"
)
