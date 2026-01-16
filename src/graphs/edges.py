from src.graphs.state import AgentState

def should_continue(state: AgentState) -> str:
    """Détermine la prochaine étape."""
    if state.get("error"):
        return "error_handler"
    if state["current_step"] == "analyzed":
        return "process"
    return "end"
