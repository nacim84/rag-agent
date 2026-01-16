from langgraph.graph import StateGraph, END
from src.graphs.state import AgentState
from src.graphs.nodes import analyze_input, process_task, generate_output
from src.graphs.edges import should_continue
from src.config.database import get_checkpointer

async def create_workflow():
    """Crée et retourne le workflow compilé."""

    # Définir le graphe
    workflow = StateGraph(AgentState)

    # Ajouter les nœuds
    workflow.add_node("analyze", analyze_input)
    workflow.add_node("process", process_task)
    workflow.add_node("generate", generate_output)

    # Définir les transitions
    workflow.set_entry_point("analyze")
    workflow.add_conditional_edges(
        "analyze",
        should_continue,
        {
            "process": "process",
            "error_handler": END,
        }
    )
    workflow.add_edge("process", "generate")
    workflow.add_edge("generate", END)

    # Compiler avec checkpointer
    checkpointer = await get_checkpointer()
    return workflow.compile(checkpointer=checkpointer)
