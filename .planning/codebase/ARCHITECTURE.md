# Architecture

**Analysis Date:** 2026-01-16

## Pattern Overview

**Overall:** LangGraph State Machine with FastAPI HTTP Layer

**Key Characteristics:**
- State-based workflow orchestration using LangGraph StateGraph
- Async-first design throughout the codebase
- PostgreSQL checkpointing for workflow persistence and recovery
- Clean separation between API layer, workflow definitions, and graph primitives
- Designed for RAG (Retrieval Augmented Generation) agent pipelines

## Layers

**API Layer:**
- Purpose: HTTP interface for external access
- Location: `src/api/`
- Contains: FastAPI application, route handlers, health checks
- Depends on: Config layer
- Used by: External clients, Docker containers

**Workflow Layer:**
- Purpose: Define complete workflow compositions
- Location: `src/agents/workflows/`
- Contains: Workflow factory functions that assemble StateGraph with nodes and edges
- Depends on: Graph layer, Config layer (for checkpointer)
- Used by: Main entry point, API layer (future routes)

**Graph Primitives Layer:**
- Purpose: Reusable building blocks for workflows
- Location: `src/graphs/`
- Contains: State definitions, node functions, edge functions
- Depends on: LangChain/LangGraph core
- Used by: Workflow layer

**Config Layer:**
- Purpose: Application configuration and database connections
- Location: `src/config/`
- Contains: Settings (pydantic-settings), database engine, checkpointer factory
- Depends on: Environment variables
- Used by: All other layers

## Data Flow

**Workflow Execution Flow:**

1. Entry point (`src/main.py`) or API creates workflow via `create_workflow()`
2. Workflow factory builds StateGraph with nodes (analyze, process, generate)
3. Initial state with messages, context passed to `app.ainvoke()`
4. StateGraph executes nodes sequentially/conditionally based on edges
5. PostgreSQL checkpointer persists state at each step
6. Final state returned with `final_output`

**State Flow Through Nodes:**

1. `analyze_input` receives state, updates `current_step` to "analyzed"
2. `should_continue` edge function routes based on error/step state
3. `process_task` receives state, updates `current_step` to "processed"
4. `generate_output` produces final result in `final_output`

**State Management:**
- Immutable state pattern: nodes return new state dicts, not mutations
- Message accumulation via `add_messages` annotated list
- Thread-based isolation via `thread_id` in config
- Persistence via PostgreSQL AsyncPostgresSaver checkpointer

## Key Abstractions

**AgentState:**
- Purpose: TypedDict defining the shape of workflow state
- Location: `src/graphs/state.py`
- Pattern: LangGraph's annotated TypedDict with `add_messages` for message history

**Node Functions:**
- Purpose: Individual processing steps in the workflow
- Location: `src/graphs/nodes.py`
- Pattern: Async functions `(state: AgentState) -> AgentState`
- Examples: `analyze_input`, `process_task`, `generate_output`

**Edge Functions:**
- Purpose: Conditional routing between nodes
- Location: `src/graphs/edges.py`
- Pattern: Sync functions `(state: AgentState) -> str` returning next node name
- Examples: `should_continue`

**Workflow Factory:**
- Purpose: Assembles complete runnable workflow
- Location: `src/agents/workflows/example_workflow.py`
- Pattern: Async function returning compiled StateGraph with checkpointer

## Entry Points

**CLI Entry Point:**
- Location: `src/main.py`
- Triggers: Direct Python execution (`python -m src.main`)
- Responsibilities: Create workflow, execute with sample input, print result

**API Entry Point:**
- Location: `src/api/app.py`
- Triggers: Uvicorn server, Docker CMD
- Responsibilities: Health check endpoint, future workflow API routes

**Worker Entry Point:**
- Location: `src/worker` (referenced in docker-compose, not yet implemented)
- Triggers: Celery worker command
- Responsibilities: Background task processing

## Error Handling

**Strategy:** State-based error propagation with conditional routing

**Patterns:**
- Errors stored in `state["error"]` field (Optional[str])
- Edge functions check for errors and route to error handlers
- `should_continue` returns "error_handler" when `state.get("error")` is truthy
- Error handler can route to END to terminate workflow gracefully

## Cross-Cutting Concerns

**Logging:**
- structlog configured in dependencies
- LOG_LEVEL configurable via environment

**Validation:**
- Pydantic models for Settings configuration
- TypedDict for state shape enforcement

**Authentication:**
- Not yet implemented at API layer
- External service auth via environment variables (API keys)

**Observability:**
- LangSmith integration via LANGCHAIN_TRACING_V2
- Automatic tracing when LANGCHAIN_API_KEY provided

**Persistence:**
- PostgreSQL for LangGraph checkpoints (workflow state)
- Redis for Celery task queue (async jobs)

---

*Architecture analysis: 2026-01-16*
