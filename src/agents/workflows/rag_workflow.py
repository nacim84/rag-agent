from langgraph.graph import StateGraph, END
from src.graphs.state import AgentState
from src.graphs.nodes import route_query, retrieve_docs, rerank_docs, generate_answer
from src.graphs.edges import should_continue
from src.config.database import get_checkpointer

async def create_rag_workflow():
    """
    Creates and returns the compiled RAG workflow.
    Workflow: route -> retrieve -> rerank -> generate -> end
    """

    # Define the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("route", route_query)
    workflow.add_node("retrieve", retrieve_docs)
    workflow.add_node("rerank", rerank_docs)
    workflow.add_node("generate", generate_answer)

    # Define transitions
    workflow.set_entry_point("route")
    
    workflow.add_conditional_edges(
        "route",
        should_continue,
        {
            "retrieve": "retrieve",
            "end": END,
        }
    )
    
    workflow.add_conditional_edges(
        "retrieve",
        should_continue,
        {
            "rerank": "rerank",
            "end": END,
        }
    )
    
    workflow.add_conditional_edges(
        "rerank",
        should_continue,
        {
            "generate": "generate",
            "end": END,
        }
    )
    
    workflow.add_edge("generate", END)

    # Compile with checkpointer for state persistence
    checkpointer = await get_checkpointer()
    return workflow.compile(checkpointer=checkpointer)
