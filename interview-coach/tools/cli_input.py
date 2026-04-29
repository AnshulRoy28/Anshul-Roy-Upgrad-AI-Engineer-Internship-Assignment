# CLI input tool - allows the Interviewer to capture candidate responses

def get_candidate_response(prompt: str) -> str:
    """
    Prints the interviewer's question to the terminal and captures the candidate's response.
    
    Args:
        prompt: The question or statement from the interviewer
        
    Returns:
        The candidate's text response
    """
    print(f"\n[Interviewer]: {prompt}\n")
    response = input("[You]: ")
    return response
