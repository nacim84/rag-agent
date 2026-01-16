# Testing Patterns

**Analysis Date:** 2026-01-16

## Test Framework

**Runner:**
- pytest >= 8.0.0
- Config: `pyproject.toml` lines 114-116

**Assertion Library:**
- pytest built-in assertions

**Async Support:**
- pytest-asyncio >= 0.23.0
- Mode: `asyncio_mode = "auto"` (automatic async test detection)

**Run Commands:**
```bash
uv run pytest                    # Run all tests
uv run pytest -v                 # Run with verbose output
uv run pytest --cov=src          # Run with coverage
uv run pytest tests/             # Run specific directory
```

## Test File Organization

**Location:**
- Separate `tests/` directory (configured in pyproject.toml)
- Currently: **No test files exist**

**Naming:**
- Expected pattern: `test_*.py` or `*_test.py`

**Expected Structure:**
```
tests/
├── conftest.py              # Shared fixtures
├── test_api/
│   └── test_app.py
├── test_graphs/
│   ├── test_nodes.py
│   ├── test_edges.py
│   └── test_state.py
└── test_config/
    └── test_settings.py
```

## Test Structure

**Suite Organization:**
```python
# Expected pattern based on pytest conventions
import pytest
from src.graphs.nodes import analyze_input
from src.graphs.state import AgentState

class TestAnalyzeInput:
    @pytest.mark.asyncio
    async def test_analyze_input_returns_analyzed_state(self):
        state = {
            "messages": [],
            "current_step": "start",
            "context": {},
            "error": None,
            "final_output": None
        }
        result = await analyze_input(state)
        assert result["current_step"] == "analyzed"
```

**Patterns:**
- Setup: Use pytest fixtures
- Teardown: Use fixture finalizers or `yield`
- Assertion: Use `assert` statements with descriptive messages

## Mocking

**Framework:**
- pytest-mock >= 3.12.0 (provides `mocker` fixture)

**Patterns:**
```python
# Expected mocking pattern for LLM calls
@pytest.fixture
def mock_llm(mocker):
    return mocker.patch(
        "langchain_openai.ChatOpenAI",
        return_value=mocker.Mock()
    )

# Expected mocking pattern for database
@pytest.fixture
def mock_checkpointer(mocker):
    return mocker.patch(
        "src.config.database.get_checkpointer",
        return_value=mocker.AsyncMock()
    )
```

**What to Mock:**
- External API calls (LLM providers, integrations)
- Database connections and checkpointers
- Environment-dependent settings

**What NOT to Mock:**
- State transformation logic in nodes
- Edge routing functions
- Pydantic validation

## Fixtures and Factories

**Test Data:**
```python
# Recommended fixture pattern for AgentState
@pytest.fixture
def base_state():
    return {
        "messages": [],
        "current_step": "start",
        "context": {},
        "error": None,
        "final_output": None
    }

@pytest.fixture
def analyzed_state(base_state):
    return {
        **base_state,
        "current_step": "analyzed",
        "context": {"analyzed": True}
    }
```

**Location:**
- Place shared fixtures in `tests/conftest.py`

## Coverage

**Requirements:** Not enforced (no minimum threshold configured)

**Tool:** pytest-cov >= 4.1.0

**View Coverage:**
```bash
uv run pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

## Test Types

**Unit Tests:**
- Scope: Individual functions (nodes, edges, utilities)
- Approach: Fast, isolated, mock external dependencies
- Priority files to test:
  - `src/graphs/nodes.py` - State transformation logic
  - `src/graphs/edges.py` - Routing decisions
  - `src/config/settings.py` - Configuration validation

**Integration Tests:**
- Scope: Full workflow execution with mocked LLM
- Approach: Test graph compilation and execution flow
- Priority: `src/agents/workflows/example_workflow.py`

**E2E Tests:**
- Framework: Not configured
- Current status: Not implemented

## Common Patterns

**Async Testing:**
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

**Error Testing:**
```python
@pytest.mark.asyncio
async def test_error_state_routes_to_handler():
    state = {
        "messages": [],
        "current_step": "analyzed",
        "context": {},
        "error": "Something went wrong",
        "final_output": None
    }
    from src.graphs.edges import should_continue
    assert should_continue(state) == "error_handler"
```

**API Testing:**
```python
from fastapi.testclient import TestClient
from src.api.app import app

def test_health_check():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

## Current Test Coverage Gaps

**Critical gaps:**
- No test files exist in the codebase
- `tests/` directory not created
- No `conftest.py` for shared fixtures

**Priority areas needing tests:**
1. `src/graphs/edges.py` - Routing logic (should_continue)
2. `src/graphs/nodes.py` - Node state transformations
3. `src/api/app.py` - Health endpoint
4. `src/config/settings.py` - Settings validation

---

*Testing analysis: 2026-01-16*
