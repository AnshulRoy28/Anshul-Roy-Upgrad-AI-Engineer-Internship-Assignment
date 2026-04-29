"""CLI input tool for capturing candidate responses."""
from typing import Dict, Any


def get_candidate_response(prompt: str, state: Dict[str, Any]) -> str:
    """
    Present a question to the candidate and capture their response.
    
    Args:
        prompt: The interviewer's question
        state: Session state (for recording conversation history)
    
    Returns:
        The candidate's response as a string
    """
    # Print the interviewer's question
    print(f"\n🎤 Interviewer: {prompt}\n")
    
    # Get candidate's response
    print("💭 You: ", end="", flush=True)
    response = input().strip()
    
    # If empty, prompt again
    while not response:
        print("💭 You: ", end="", flush=True)
        response = input().strip()
    
    return response
