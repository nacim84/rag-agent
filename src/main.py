import asyncio
from uuid import uuid4
from langchain_core.messages import HumanMessage
from src.agents.workflows.example_workflow import create_workflow

async def main():
    # Créer le workflow
    app = await create_workflow()

    # Configuration du thread
    thread_id = str(uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # Exécuter
    initial_state = {
        "messages": [HumanMessage(content="Traite cette tâche")],
        "current_step": "start",
        "context": {},
        "error": None,
        "final_output": None,
    }

    result = await app.ainvoke(initial_state, config)
    print(f"Résultat: {result['final_output']}")

if __name__ == "__main__":
    asyncio.run(main())
