# Codebase Structure

**Analysis Date:** 2026-01-16

## Directory Layout

```
rag-agent/
├── src/                    # Application source code
│   ├── agents/             # Agent workflow definitions
│   │   └── workflows/      # Complete workflow compositions
│   ├── api/                # FastAPI HTTP layer
│   ├── config/             # Configuration and database setup
│   └── graphs/             # LangGraph primitives (state, nodes, edges)
├── scripts/                # Database and utility scripts
├── n8n_assets/             # N8N workflow JSON exports
├── .planning/              # Planning documents
│   └── codebase/           # Codebase analysis documents
├── docker-compose.yml      # Multi-container orchestration
├── Dockerfile              # Production container build
├── Dockerfile.dev          # Development container build
├── pyproject.toml          # Python project config (uv/pip)
├── uv.lock                 # Dependency lockfile
├── .env.example            # Environment variable template
└── .python-version         # Python version (3.11)
```

## Directory Purposes

**src/:**
- Purpose: All application Python code
- Contains: Agents, API, config, graphs modules
- Key files: `main.py` (CLI entry point)

**src/agents/:**
- Purpose: High-level agent definitions
- Contains: Workflow subdirectory
- Key files: None yet (future: base agent classes)

**src/agents/workflows/:**
- Purpose: Complete workflow factory functions
- Contains: Workflow files that compose nodes/edges into runnable graphs
- Key files: `example_workflow.py`

**src/api/:**
- Purpose: HTTP interface layer
- Contains: FastAPI application and route handlers
- Key files: `app.py`

**src/config/:**
- Purpose: Centralized configuration management
- Contains: Settings class, database connections, checkpointer factory
- Key files: `settings.py`, `database.py`

**src/graphs/:**
- Purpose: Reusable LangGraph building blocks
- Contains: State definitions, node functions, edge functions
- Key files: `state.py`, `nodes.py`, `edges.py`

**scripts/:**
- Purpose: Database initialization and utility scripts
- Contains: SQL scripts for PostgreSQL setup
- Key files: `init_db.sql`

**n8n_assets/:**
- Purpose: N8N workflow definitions for external automation
- Contains: JSON exports of N8N workflows
- Key files: `Add_Documents_Workflow.json`

## Key File Locations

**Entry Points:**
- `src/main.py`: CLI workflow execution
- `src/api/app.py`: FastAPI HTTP server

**Configuration:**
- `src/config/settings.py`: Pydantic settings with env vars
- `src/config/database.py`: SQLAlchemy engine, LangGraph checkpointer
- `.env.example`: Environment variable documentation
- `pyproject.toml`: Dependencies and tool configuration

**Core Logic:**
- `src/graphs/state.py`: AgentState TypedDict
- `src/graphs/nodes.py`: Node functions (analyze, process, generate)
- `src/graphs/edges.py`: Edge/routing functions
- `src/agents/workflows/example_workflow.py`: Workflow composition

**Infrastructure:**
- `docker-compose.yml`: PostgreSQL, Redis, N8N, Qdrant services
- `Dockerfile`: Production multi-stage build
- `scripts/init_db.sql`: Database schema initialization

**Testing:**
- `tests/` (not yet created, configured in pyproject.toml)

## Naming Conventions

**Files:**
- Snake_case for Python files: `example_workflow.py`, `settings.py`
- Lowercase with underscores: `init_db.sql`
- Title_Case for workflow JSON: `Add_Documents_Workflow.json`

**Directories:**
- Lowercase, plural for collections: `agents`, `graphs`, `workflows`
- Lowercase, singular for purpose: `api`, `config`

**Python:**
- Classes: PascalCase (`AgentState`, `Settings`)
- Functions: snake_case (`create_workflow`, `analyze_input`)
- Constants: UPPER_SNAKE_CASE (`DATABASE_URL`, `APP_NAME`)

## Where to Add New Code

**New Workflow:**
- Primary code: `src/agents/workflows/new_workflow.py`
- Create factory function `create_workflow()` returning compiled StateGraph
- Import nodes/edges from `src/graphs/` or create workflow-specific ones

**New Node Function:**
- Implementation: `src/graphs/nodes.py`
- Pattern: `async def node_name(state: AgentState) -> AgentState`
- Must return new state dict, not mutate

**New Edge Function:**
- Implementation: `src/graphs/edges.py`
- Pattern: `def edge_name(state: AgentState) -> str`
- Return string matching node name or "end"

**New API Endpoint:**
- Implementation: `src/api/app.py` (or new router file)
- Use `@app.get()` / `@app.post()` decorators
- For routers: create `src/api/routes/` directory

**New State Fields:**
- Modify: `src/graphs/state.py`
- Add field to `AgentState` TypedDict
- Update nodes that read/write the field

**New Configuration:**
- Add env var: `src/config/settings.py` in Settings class
- Document: `.env.example`

**Utilities:**
- Shared helpers: `src/utils/` (create directory)
- Integration clients: `src/integrations/` (create directory)

**Tests:**
- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- Pattern: `test_<module>.py`

## Special Directories

**.planning/:**
- Purpose: Planning and analysis documentation
- Generated: By GSD mapping commands
- Committed: Yes (for team reference)

**n8n_assets/:**
- Purpose: External N8N workflow definitions
- Generated: Exported from N8N UI
- Committed: Yes (version control for automations)

**secrets/:**
- Purpose: Mounted credentials for Google APIs, etc.
- Generated: Manual setup
- Committed: No (in .gitignore)

**.venv/:**
- Purpose: Python virtual environment
- Generated: By uv/pip
- Committed: No (in .gitignore)

---

*Structure analysis: 2026-01-16*
