"""AI Mock Interview Coach - ADK-Based Entry Point.

This version uses Google's Agent Development Kit (ADK) patterns for a truly agentic system.
"""
import sys
from typing import Dict

from google.genai import Client
import config
from adk_agents.orchestrator import InterviewOrchestrator


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 60)
    print("🎯 AI Mock Interview Coach (ADK-Powered)")
    print("=" * 60)
    print("\nWelcome! This is an advanced multi-agent system powered by")
    print("Google's Agent Development Kit (ADK) patterns.")
    print("\nFeatures:")
    print("  • Adaptive strategy adjustment")
    print("  • Outcome prediction")
    print("  • Pattern detection")
    print("  • Agent memory and reflection")
    print("\nLet's start by understanding what you're preparing for.\n")


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
    
    print("\n🔧 Advanced Features")
    print("   Enable adaptive strategy? (y/n)")
    adaptive = input("   → ").strip().lower() == 'y'
    
    print("   Enable outcome prediction? (y/n)")
    prediction = input("   → ").strip().lower() == 'y'
    
    return {
        "role": role,
        "background": background if background else "No background provided",
        "focus_area": focus,
        "adaptive_strategy": adaptive,
        "outcome_prediction": prediction,
    }


def main():
    """Main entry point for ADK-based interview coach."""
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
    
    # Initialize orchestrator
    orchestrator = InterviewOrchestrator(client)
    
    # Initialize session
    orchestrator.initialize_session(
        role=candidate_info["role"],
        background=candidate_info["background"],
        focus_area=candidate_info["focus_area"],
    )
    
    # Run profiler phase
    profiler_result = orchestrator.run_profiler_phase()
    
    # Start interview
    print("\n" + "=" * 60)
    print("🎬 Let's begin the interview!")
    print("=" * 60)
    
    # Run interview loop with adaptive features
    turn = 1
    while turn <= config.MAX_INTERVIEW_TURNS:
        should_continue = orchestrator.run_interview_turn(turn)
        
        # Enable adaptive strategy if requested
        if candidate_info["adaptive_strategy"]:
            orchestrator.enable_adaptive_strategy()
        
        # Enable outcome prediction if requested
        if candidate_info["outcome_prediction"] and turn == 3:
            prediction = orchestrator.enable_outcome_prediction()
            if prediction:
                print(f"\n🔮 Predicted Outcome: {prediction.get('outcome', 'N/A')}")
                print(f"   Confidence: {prediction.get('confidence', 'N/A')}%")
        
        turn += 1
        
        if not should_continue:
            break
    
    # Generate coaching report
    print("\n" + "=" * 60)
    print("🎓 Interview Complete!")
    print("=" * 60)
    
    coach_result = orchestrator.run_coach_phase()
    
    # Display report
    print("\n" + "=" * 60)
    print("📋 YOUR COACHING REPORT")
    print("=" * 60)
    print(coach_result["report"])
    
    # Display additional insights
    print("\n" + "=" * 60)
    print("🧠 AGENT INSIGHTS")
    print("=" * 60)
    
    insights = orchestrator.get_agent_insights()
    
    print("\n📊 Performance Benchmark:")
    benchmark = insights["coach"].get("benchmark", {})
    if benchmark:
        print(f"   Readiness: {benchmark.get('readiness_level', 'N/A')}")
        print(f"   Percentile: {benchmark.get('percentile', 'N/A')}")
    
    print("\n🎯 Skill Gaps Identified:")
    skill_gaps = insights["coach"].get("skill_gaps", {})
    if skill_gaps and isinstance(skill_gaps, dict):
        gaps_list = skill_gaps.get("gaps", [])
        for i, gap in enumerate(gaps_list[:3], 1):
            if isinstance(gap, dict):
                print(f"   {i}. {gap.get('description', 'N/A')} (Severity: {gap.get('severity', 'N/A')})")
    
    print("\n📈 Answer Patterns Detected:")
    patterns = insights["evaluator"].get("answer_patterns", {})
    if patterns and isinstance(patterns, dict):
        strengths = patterns.get("consistent_strengths", [])
        if strengths:
            print(f"   Strengths: {', '.join(strengths[:2])}")
        weaknesses = patterns.get("consistent_weaknesses", [])
        if weaknesses:
            print(f"   Weaknesses: {', '.join(weaknesses[:2])}")
    
    # Display orchestration metadata
    print("\n" + "=" * 60)
    print("🤖 SYSTEM METADATA")
    print("=" * 60)
    print(f"   Total Agent Calls: {orchestrator.metadata['total_agent_calls']}")
    print(f"   Interview Turns: {turn - 1}")
    print(f"   Adaptive Strategy: {'Enabled' if candidate_info['adaptive_strategy'] else 'Disabled'}")
    print(f"   Outcome Prediction: {'Enabled' if candidate_info['outcome_prediction'] else 'Disabled'}")
    
    print("\n" + "=" * 60)
    print("✨ Thank you for using AI Mock Interview Coach (ADK-Powered)!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
