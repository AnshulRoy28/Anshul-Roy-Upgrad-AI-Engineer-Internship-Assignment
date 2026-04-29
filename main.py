"""AI Mock Interview Coach - CLI Entry Point."""
import json
import sys
from typing import Dict, Any

from google.genai import Client
import config
import state


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 60)
    print("🎯 AI Mock Interview Coach")
    print("=" * 60)
    print("\nWelcome! I'll conduct a mock interview to help you prepare.")
    print("Let's start by understanding what you're preparing for.\n")


def collect_candidate_info() -> Dict[str, str]:
    """Collect candidate information via CLI."""
    print("📋 Target Role")
    print("   (e.g., 'Product Manager', 'Frontend Engineer Intern', 'Data Analyst')")
    role = input("   → ").strip()
    while not role:
        print("   Please enter a role:")
        role = input("   → ").strip()
    
    print("\n📝 Background (optional)")
    print("   (2-3 lines about your experience, or press Enter to skip)")
    background = input("   → ").strip()
    
    print("\n🎯 Focus Area")
    print("   Choose: behavioral / technical / case / mixed")
    focus = input("   → ").strip().lower()
    while focus not in ["behavioral", "technical", "case", "mixed"]:
        print("   Please choose: behavioral / technical / case / mixed")
        focus = input("   → ").strip().lower()
    
    return {
        "role": role,
        "background": background if background else "No background provided",
        "focus_area": focus,
    }


def run_profiler(client: Client, candidate_info: Dict[str, str]) -> Dict[str, Any]:
    """Run the Profiler agent to create interview strategy."""
    print("\n🔍 Analyzing your profile and creating interview strategy...")
    
    from agents import get_profiler_prompt
    prompt_text = get_profiler_prompt()
    
    user_message = f"""
Candidate Information:
- Role: {candidate_info['role']}
- Background: {candidate_info['background']}
- Focus Area: {candidate_info['focus_area']}

Create the interview strategy JSON.
"""
    
    response = client.models.generate_content(
        model=config.MODEL,
        contents=user_message,
        config={
            "system_instruction": prompt_text,
            "temperature": 0.7,
            "response_mime_type": "application/json",
        },
    )
    
    strategy = json.loads(response.text)
    print("✅ Strategy created!\n")
    return strategy


def run_interview_turn(
    client: Client,
    session_state: Dict[str, Any],
    turn_number: int,
) -> bool:
    """
    Run a single interview turn (question + answer + evaluation).
    
    Returns:
        True if interview should continue, False if it should end
    """
    from agents import get_interviewer_prompt, get_turn_evaluator_prompt
    interviewer_prompt = get_interviewer_prompt()
    evaluator_prompt = get_turn_evaluator_prompt()
    
    # Build context for interviewer
    strategy = session_state[state.SESSION_STRATEGY]
    last_signal = session_state.get(state.LAST_EVALUATOR_SIGNAL, "advance")
    history = session_state[state.CONVERSATION_HISTORY]
    
    context = f"""
Session Strategy:
{json.dumps(strategy, indent=2)}

Current Turn: {turn_number}
Last Evaluator Signal: {last_signal}

Conversation History:
{json.dumps(history, indent=2)}

Based on the strategy and signal, generate your next question. Remember to follow the competency pillars and difficulty arc.
"""
    
    # Interviewer generates question
    interviewer_response = client.models.generate_content(
        model=config.MODEL,
        contents=context,
        config={
            "system_instruction": interviewer_prompt,
            "temperature": 0.8,
        },
    )
    
    question = interviewer_response.text.strip()
    
    # Present question and get answer
    print(f"\n🎤 Interviewer: {question}\n")
    print("💭 You: ", end="", flush=True)
    answer = input().strip()
    
    while not answer:
        print("💭 You: ", end="", flush=True)
        answer = input().strip()
    
    # Record conversation
    state.add_conversation_turn(session_state, question, answer)
    
    # Evaluator scores the answer
    eval_context = f"""
Session Strategy:
{json.dumps(strategy, indent=2)}

Current Turn: {turn_number}

Question Asked: {question}

Candidate's Answer: {answer}

Evaluate this answer and provide your JSON assessment.
"""
    
    evaluator_response = client.models.generate_content(
        model=config.MODEL,
        contents=eval_context,
        config={
            "system_instruction": evaluator_prompt,
            "temperature": 0.3,
            "response_mime_type": "application/json",
        },
    )
    
    evaluation = json.loads(evaluator_response.text)
    evaluation["turn"] = turn_number
    
    # Store evaluation
    state.append_turn_score(session_state, evaluation)
    session_state[state.LAST_EVALUATOR_SIGNAL] = evaluation["next_move"]
    
    # Check if interview should end
    if evaluation["next_move"] == "wrap_up" or turn_number >= config.MAX_INTERVIEW_TURNS:
        return False
    
    return True


def run_coach(client: Client, session_state: Dict[str, Any]) -> str:
    """Run the Coach agent to generate final feedback."""
    print("\n📊 Analyzing your interview performance...")
    
    from agents import get_coach_prompt
    coach_prompt = get_coach_prompt()
    
    context = f"""
Complete Session Data:

Candidate Role: {session_state[state.CANDIDATE_ROLE]}
Focus Area: {session_state[state.FOCUS_AREA]}

Session Strategy:
{json.dumps(session_state[state.SESSION_STRATEGY], indent=2)}

Conversation History:
{json.dumps(session_state[state.CONVERSATION_HISTORY], indent=2)}

Turn Scores:
{json.dumps(session_state[state.TURN_SCORES], indent=2)}

Generate your comprehensive coaching report in Markdown format.
"""
    
    response = client.models.generate_content(
        model=config.MODEL,
        contents=context,
        config={
            "system_instruction": coach_prompt,
            "temperature": 0.7,
        },
    )
    
    return response.text


def main():
    """Main entry point."""
    # Check API key
    if not config.GOOGLE_API_KEY:
        print("❌ Error: GOOGLE_API_KEY not found in environment")
        print("   Please set it in your .env file")
        sys.exit(1)
    
    # Initialize client
    client = Client(api_key=config.GOOGLE_API_KEY)
    
    # Print banner and collect info
    print_banner()
    candidate_info = collect_candidate_info()
    
    # Initialize session state
    session_state = state.initialize_state(
        role=candidate_info["role"],
        background=candidate_info["background"],
        focus_area=candidate_info["focus_area"],
    )
    
    # Run profiler
    strategy = run_profiler(client, candidate_info)
    session_state[state.SESSION_STRATEGY] = strategy
    
    # Start interview
    print("\n" + "=" * 60)
    print("🎬 Let's begin the interview!")
    print("=" * 60)
    
    # Run interview loop
    turn = 1
    while turn <= config.MAX_INTERVIEW_TURNS:
        should_continue = run_interview_turn(client, session_state, turn)
        state.increment_turn(session_state)
        turn += 1
        
        if not should_continue:
            break
    
    # Generate coaching report
    print("\n" + "=" * 60)
    print("🎓 Interview Complete!")
    print("=" * 60)
    
    coaching_report = run_coach(client, session_state)
    session_state[state.COACHING_REPORT] = coaching_report
    
    # Display report
    print("\n" + "=" * 60)
    print("📋 YOUR COACHING REPORT")
    print("=" * 60)
    print(coaching_report)
    print("\n" + "=" * 60)
    print("✨ Thank you for using AI Mock Interview Coach!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
