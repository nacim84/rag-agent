from langchain_core.messages import AIMessage, HumanMessage
from src.graphs.state import AgentState

async def analyze_input(state: AgentState) -> AgentState:
    """Nœud d'analyse de l'entrée."""
    # Logique d'analyse
    return {
        **state,
        "current_step": "analyzed",
        "context": {"analyzed": True}
    }

async def process_task(state: AgentState) -> AgentState:
    """Nœud de traitement principal."""
    # Logique de traitement
    return {
        **state,
        "current_step": "processed"
    }

async def generate_output(state: AgentState) -> AgentState:
    """Nœud de génération de sortie."""
    return {
        **state,
        "current_step": "completed",
        "final_output": {"result": "success"}
    }
