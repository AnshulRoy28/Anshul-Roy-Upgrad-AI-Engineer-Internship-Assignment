# Turn Evaluator Agent - evaluates each answer and provides signal

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from config import MODEL, load_prompt, MAX_INTERVIEW_TURNS
from state import schema
import json

# Load the turn evaluator prompt
TURN_EVALUATOR_PROMPT = load_prompt("turn_evaluator.md")


def after_evaluator_callback(callback_context: CallbackContext):
    """
    Callback that runs after the Turn Evaluator completes.
    - Appends the score to turn_scores
    - Increments current_turn
    - Checks termination conditions
    """
    state = callback_context.state
    
    # Get the evaluator's output (should be JSON)
    evaluator_output = state.get(schema.LAST_EVALUATOR_SIGNAL, "{}")
    
    try:
        score = json.loads(evaluator_output)
        
        # Append to turn_scores
        schema.append_turn_score(state, score)
        
        # Increment turn counter
        schema.increment_turn(state)
        
        # Check termination conditions
        current_turn = state.get(schema.CURRENT_TURN, 0)
        next_move = score.get("next_move", "advance")
        
        if current_turn >= MAX_INTERVIEW_TURNS or next_move == "wrap_up":
            schema.mark_interview_complete(state)
            
    except json.JSONDecodeError:
        # If JSON parsing fails, still increment turn and check max turns
        schema.increment_turn(state)
        if state.get(schema.CURRENT_TURN, 0) >= MAX_INTERVIEW_TURNS:
            schema.mark_interview_complete(state)


# Create the Turn Evaluator agent
turn_evaluator_agent = LlmAgent(
    name="TurnEvaluator",
    model=MODEL,
    instruction=TURN_EVALUATOR_PROMPT,
    description="Evaluates candidate answers and provides next move signal",
    output_key=schema.LAST_EVALUATOR_SIGNAL,
    include_contents='none',  # Stateless - only uses current turn data
    after_agent_callback=after_evaluator_callback
)
