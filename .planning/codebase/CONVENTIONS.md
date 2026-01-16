# Coding Conventions

**Analysis Date:** 2026-01-16

## Naming Patterns

**Files:**
- snake_case for Python modules: `example_workflow.py`, `settings.py`
- Directories use snake_case: `agents/workflows/`

**Functions:**
- snake_case for all functions: `create_workflow()`, `get_checkpointer()`, `health_check()`
- Async functions prefixed implicitly by usage: `async def analyze_input()`

**Variables:**
- snake_case for local variables: `thread_id`, `initial_state`
- SCREAMING_SNAKE_CASE for environment/config constants: `DATABASE_URL`, `OPENAI_API_KEY`

**Types:**
- PascalCase for classes and TypedDict: `AgentState`, `Settings`
- Type annotations on all function signatures

## Code Style

**Formatting:**
- Tool: Ruff (configured in `pyproject.toml`)
- Line length: 100 characters
- Target Python version: 3.11

**Linting:**
- Tool: Ruff
- Rules enabled: `["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]`
- E501 (line too long) is ignored
- Config location: `pyproject.toml` lines 101-107

**Type Checking:**
- Tool: mypy in strict mode
- `ignore_missing_imports = true`
- Config location: `pyproject.toml` lines 109-112

## Import Organization

**Order:**
1. Standard library imports (`asyncio`, `typing`, `uuid`, `functools`)
2. Third-party imports (`fastapi`, `pydantic`, `langchain`, `langgraph`)
3. Local imports (`src.config.settings`, `src.graphs.state`)

**Path Aliases:**
- None configured; use full `src.` prefix for local imports
- Example: `from src.config.settings import settings`

## Error Handling

**Patterns:**
- State-based error tracking via `error` field in `AgentState`
- Conditional edge routing to `error_handler` on error presence
- Example from `src/graphs/edges.py`:
```python
def should_continue(state: AgentState) -> str:
    if state.get("error"):
        return "error_handler"
```

**No explicit try/except blocks observed** - error handling is implicit through state management.

## Logging

**Framework:** structlog (dependency, not yet implemented in code)

**Patterns:**
- Currently uses `print()` for output in `src/main.py`
- LOG_LEVEL configured via environment variable

## Comments

**When to Comment:**
- Docstrings for all classes and public functions (observed)
- French language used for comments and docstrings

**Docstring Format:**
```python
"""Description courte de la fonction."""
```

Single-line docstrings without parameter documentation.

## Function Design

**Size:** Small, focused functions (~5-15 lines)

**Parameters:**
- State objects passed as single parameter for graph nodes
- Type hints required on all parameters

**Return Values:**
- Full state dict returned from node functions (immutable spread pattern)
- Pattern:
```python
return {
    **state,
    "current_step": "analyzed",
    "context": {"analyzed": True}
}
```

## Module Design

**Exports:**
- No `__init__.py` files present
- Direct imports from modules
- Single responsibility per module

**Barrel Files:**
- Not used in this codebase

## Async Patterns

**Convention:** Async-first design
- All node functions are `async def`
- Database operations use async SQLAlchemy
- FastAPI endpoints are async

**Pattern:**
```python
async def main():
    app = await create_workflow()
    result = await app.ainvoke(initial_state, config)
```

## Configuration

**Settings Pattern:**
- Pydantic Settings for configuration (`src/config/settings.py`)
- Singleton via `@lru_cache` decorator
- Environment variables with `.env` file support
- Optional fields use `Optional[str] = None`

**Pattern:**
```python
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

## State Management (LangGraph)

**State Definition:**
- TypedDict with Annotated fields for message handling
- Located in `src/graphs/state.py`

**Pattern:**
```python
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    current_step: str
    context: dict
    error: Optional[str]
    final_output: Optional[dict]
```

---

*Convention analysis: 2026-01-16*
