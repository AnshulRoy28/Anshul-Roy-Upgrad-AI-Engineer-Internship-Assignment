# Main entry point for the AI Mock Interview Coach

import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from config import APP_NAME
from orchestration.pipeline import interview_pipeline
from state import schema


def print_banner():
    """Print welcome banner."""
    print("=" * 60)
    print("  AI MOCK INTERVIEW COACH")
    print("=" * 60)
    print()


def collect_input() -> dict:
    """Collect candidate information from terminal."""
    print("Let's set up your mock interview.\n")
    
    role = input("Target role (e.g., Product Manager, Data Analyst): ").strip()
    
    print("\nOptional: Provide a 2-3 line background or resume snippet")
    print("(Press Enter to skip)")
    background = input("> ").strip()
    if not background:
        background = "No background provided"
    
    print("\nFocus area:")
    print("  1. Behavioral")
    print("  2. Technical")
    print("  3. Case")
    print("  4. Mixed")
    focus_choice = input("Choose (1-4): ").strip()
    
    focus_map = {
        "1": "behavioral",
        "2": "technical",
        "3": "case",
        "4": "mixed"
    }
    focus_area = focus_map.get(focus_choice, "mixed")
    
    return {
        schema.CANDIDATE_ROLE: role,
        schema.CANDIDATE_BACKGROUND: background,
        schema.FOCUS_AREA: focus_area,
        schema.CURRENT_TURN: 0,
        schema.INTERVIEW_COMPLETE: False,
        schema.CONVERSATION_HISTORY: [],
        schema.TURN_SCORES: []
    }


async def run_interview():
    """Main interview execution."""
    print_banner()
    
    # Collect input
    initial_state = collect_input()
    
    print("\n" + "=" * 60)
    print("  STARTING INTERVIEW")
    print("=" * 60 + "\n")
    
    # Set up session service
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id="candidate_001"
    )
    
    # Seed the session state
    session.state.update(initial_state)
    
    # Create runner
    runner = Runner(
        agent=interview_pipeline,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    # Create initial message to trigger the pipeline
    # The profiler will read from state, not from this message
    initial_message = types.Content(
        role='user',
        parts=[types.Part(text="Begin interview")]
    )
    
    # Run the pipeline
    try:
        async for event in runner.run_async(
            user_id="candidate_001",
            session_id=session.id,
            new_message=initial_message
        ):
            # We can log events here if needed
            pass
    except Exception as e:
        print(f"\nError during interview: {e}")
        return
    
    # Get final session state
    final_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id="candidate_001",
        session_id=session.id
    )
    
    # Print the coaching report
    coaching_report = final_session.state.get(schema.COACHING_REPORT, "No report generated")
    
    print("\n" + "=" * 60)
    print("  INTERVIEW COMPLETE - YOUR FEEDBACK")
    print("=" * 60 + "\n")
    print(coaching_report)
    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(run_interview())
