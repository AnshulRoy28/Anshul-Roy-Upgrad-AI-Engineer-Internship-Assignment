"""Automated demo of the interview coach (non-interactive)."""
import json
from google.genai import Client
import config
import state
from agents import get_profiler_prompt, get_interviewer_prompt, get_turn_evaluator_prompt, get_coach_prompt

# Sample candidate info
DEMO_CANDIDATE = {
    "role": "Product Manager",
    "background": "2 years as Associate PM at a B2B SaaS startup",
    "focus_area": "behavioral"
}

# Sample answers (simulating a candidate)
DEMO_ANSWERS = [
    "In my previous role, I led a feature launch for our analytics dashboard. The situation was that customers were requesting better reporting capabilities. I coordinated with a team of 5 engineers, prioritized features based on user research with 20+ customers, and we launched in 3 months. The result was a 25% increase in user engagement.",
    
    "I faced a conflict when engineering wanted to delay a feature for technical debt, but sales had promised it to a key client. I organized a meeting with both teams, presented data on the technical risks and business impact, and we agreed on a phased approach - delivering core functionality on time while scheduling the refactor for the next sprint.",
    
    "I prioritize features using a combination of user impact, business value, and technical feasibility. For example, I created a scoring matrix that weighted customer requests by revenue potential and implementation effort. This helped us focus on high-impact, achievable wins.",
    
    "When stakeholders disagree, I try to understand their underlying concerns first. In one case, marketing wanted a flashy feature while product wanted to focus on stability. I facilitated a workshop where we mapped features to our OKRs, which helped everyone align on priorities.",
    
    "I measure success through both quantitative and qualitative metrics. For the analytics feature, I tracked adoption rate, user engagement, and customer satisfaction scores. We also conducted follow-up interviews to understand what was working and what needed improvement."
]

def run_demo():
    """Run a complete demo interview."""
    print("\n" + "="*60)
    print("🎯 AI Mock Interview Coach - DEMO MODE")
    print("="*60)
    print("\nRunning automated demo with sample candidate...")
    print(f"Role: {DEMO_CANDIDATE['role']}")
    print(f"Background: {DEMO_CANDIDATE['background']}")
    print(f"Focus: {DEMO_CANDIDATE['focus_area']}")
    
    client = Client(api_key=config.GOOGLE_API_KEY)
    
    # Initialize session
    session_state = state.initialize_state(
        role=DEMO_CANDIDATE["role"],
        background=DEMO_CANDIDATE["background"],
        focus_area=DEMO_CANDIDATE["focus_area"]
    )
    
    # Step 1: Profiler
    print("\n" + "="*60)
    print("STEP 1: Creating Interview Strategy")
    print("="*60)
    
    profiler_prompt = get_profiler_prompt()
    user_message = f"""
Candidate Information:
- Role: {DEMO_CANDIDATE['role']}
- Background: {DEMO_CANDIDATE['background']}
- Focus Area: {DEMO_CANDIDATE['focus_area']}

Create the interview strategy JSON.
"""
    
    response = client.models.generate_content(
        model=config.MODEL,
        contents=user_message,
        config={
            "system_instruction": profiler_prompt,
            "temperature": 0.7,
            "response_mime_type": "application/json",
        },
    )
    
    strategy = json.loads(response.text)
    session_state[state.SESSION_STRATEGY] = strategy
    print("✅ Strategy created!")
    print(f"Competency Pillars: {', '.join(strategy['competency_pillars'])}")
    
    # Step 2: Interview Loop
    print("\n" + "="*60)
    print("STEP 2: Conducting Interview")
    print("="*60)
    
    interviewer_prompt = get_interviewer_prompt()
    evaluator_prompt = get_turn_evaluator_prompt()
    
    for turn_num in range(1, min(len(DEMO_ANSWERS) + 1, 6)):
        print(f"\n--- Turn {turn_num} ---")
        
        # Interviewer asks question
        last_signal = session_state.get(state.LAST_EVALUATOR_SIGNAL, "advance")
        context = f"""
Session Strategy:
{json.dumps(strategy, indent=2)}

Current Turn: {turn_num}
Last Evaluator Signal: {last_signal}

Conversation History:
{json.dumps(session_state[state.CONVERSATION_HISTORY], indent=2)}

Generate your next question.
"""
        
        interviewer_response = client.models.generate_content(
            model=config.MODEL,
            contents=context,
            config={
                "system_instruction": interviewer_prompt,
                "temperature": 0.8,
            },
        )
        
        question = interviewer_response.text.strip()
        print(f"\n🎤 Interviewer: {question}")
        
        # Candidate answers (from demo answers)
        answer = DEMO_ANSWERS[turn_num - 1]
        print(f"\n💭 Candidate: {answer}")
        
        # Record conversation
        state.add_conversation_turn(session_state, question, answer)
        
        # Evaluator scores
        eval_context = f"""
Session Strategy:
{json.dumps(strategy, indent=2)}

Current Turn: {turn_num}

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
        evaluation["turn"] = turn_num
        
        state.append_turn_score(session_state, evaluation)
        session_state[state.LAST_EVALUATOR_SIGNAL] = evaluation["next_move"]
        
        print(f"\n📊 Scores: {evaluation['scores']}")
        print(f"📍 Next Move: {evaluation['next_move']}")
        
        if evaluation["next_move"] == "wrap_up":
            break
    
    # Step 3: Coach
    print("\n" + "="*60)
    print("STEP 3: Generating Coaching Report")
    print("="*60)
    
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
    
    coaching_report = response.text
    
    # Display report
    print("\n" + "="*60)
    print("📋 COACHING REPORT")
    print("="*60)
    print(coaching_report)
    print("\n" + "="*60)
    print("✨ Demo Complete!")
    print("="*60)


if __name__ == "__main__":
    run_demo()
