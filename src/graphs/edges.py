from src.graphs.state import AgentState

def should_continue(state: AgentState) -> str:
    """
    Controls the flow between nodes.
    Currently linear: route -> retrieve -> rerank -> generate
    """
    if state.get("error"):
        return "end" # Early exit on error
        
    step = state["current_step"]
    
    if step == "routed":
        return "retrieve"
    elif step == "retrieved":
        return "rerank"
    elif step == "reranked":
        return "generate"
    elif step == "completed":
        return "end"
        
    return "end"