import asyncio
from uuid import uuid4
from langchain_core.messages import HumanMessage
from src.agents.workflows.example_workflow import create_workflow

async def main():
    # Create the workflow
    app = await create_workflow()

    # Thread configuration
    thread_id = str(uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # Execute
    initial_state = {
        "messages": [HumanMessage(content="Process this task")],
        "current_step": "start",
        "context": {},
        "error": None,
        "final_output": None,
    }

    result = await app.ainvoke(initial_state, config)
    print(f"Result: {result['final_output']}")

if __name__ == "__main__":
    asyncio.run(main())
