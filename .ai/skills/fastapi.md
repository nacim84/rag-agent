# FastAPI - Compétences et Bonnes Pratiques

## Vue d'ensemble

FastAPI est un framework web moderne et rapide pour construire des APIs avec Python. Il est basé sur les annotations de type Python standard et offre des performances élevées, une facilité d'utilisation, et une documentation interactive automatique.

## Concepts Clés

### 1. Application de Base

```python
from fastapi import FastAPI

app = FastAPI(
    title="LangGraph Workflow API",
    description="API pour orchestrer des workflows agentiques",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 2. Path Operations (Routes)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float

# GET
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

# POST
@app.post("/items/", response_model=Item, status_code=201)
async def create_item(item: Item):
    return item

# PUT
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    return item

# DELETE
@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    # Logique de suppression
    return None
```

### 3. Request Validation avec Pydantic

```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class WorkflowInput(BaseModel):
    workflow_id: str = Field(..., min_length=1, max_length=100)
    payload: dict
    timeout: int = Field(default=30, ge=1, le=300)

    @validator('workflow_id')
    def validate_workflow_id(cls, v):
        if not v.startswith('wf_'):
            raise ValueError('workflow_id must start with "wf_"')
        return v

@app.post("/workflows/execute")
async def execute_workflow(input: WorkflowInput):
    # L'input est automatiquement validé
    return {"status": "processing", "workflow_id": input.workflow_id}
```

### 4. Response Models

```python
from typing import List

class WorkflowResult(BaseModel):
    workflow_id: str
    status: str
    output: dict | None = None
    error: str | None = None

@app.post("/workflows/execute", response_model=WorkflowResult)
async def execute_workflow(input: WorkflowInput):
    # FastAPI filtre automatiquement les champs non définis dans le response_model
    result = {
        "workflow_id": input.workflow_id,
        "status": "completed",
        "output": {"result": "success"},
        "internal_debug_info": "this won't be included"  # Filtré
    }
    return result

@app.get("/workflows/", response_model=List[WorkflowResult])
async def list_workflows():
    return [...]
```

### 5. Dependency Injection

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Dépendance pour la session DB
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Dépendance pour l'authentification
async def get_current_user(token: str = Header(...)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# Utilisation des dépendances
@app.get("/workflows/")
async def list_workflows(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # db et current_user sont injectés automatiquement
    workflows = await get_user_workflows(db, current_user.id)
    return workflows
```

### 6. Middleware

**Middleware de traçage du temps:**

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

**CORS Middleware:**

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "https://yourdomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 7. Background Tasks

```python
from fastapi import BackgroundTasks

def send_notification(email: str, message: str):
    """Tâche asynchrone d'envoi d'email."""
    # Logique d'envoi
    print(f"Sending notification to {email}: {message}")

@app.post("/workflows/execute")
async def execute_workflow(
    input: WorkflowInput,
    background_tasks: BackgroundTasks
):
    # Ajouter une tâche de fond
    background_tasks.add_task(
        send_notification,
        email="user@example.com",
        message=f"Workflow {input.workflow_id} started"
    )

    return {"status": "processing"}
```

### 8. Lifespan Events

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    # Initialiser les connexions DB, Redis, etc.
    await init_db()
    await init_redis()

    yield

    # Shutdown
    print("Shutting down...")
    # Fermer les connexions
    await close_db()
    await close_redis()

app = FastAPI(lifespan=lifespan)
```

### 9. Exception Handling

```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class WorkflowNotFoundError(Exception):
    def __init__(self, workflow_id: str):
        self.workflow_id = workflow_id

@app.exception_handler(WorkflowNotFoundError)
async def workflow_not_found_handler(request: Request, exc: WorkflowNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Workflow not found",
            "workflow_id": exc.workflow_id
        }
    )

@app.get("/workflows/{workflow_id}")
async def get_workflow(workflow_id: str):
    workflow = await find_workflow(workflow_id)
    if not workflow:
        raise WorkflowNotFoundError(workflow_id)
    return workflow
```

### 10. WebSockets

```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws/workflows/{workflow_id}")
async def workflow_stream(websocket: WebSocket, workflow_id: str):
    await websocket.accept()
    try:
        # Streamer les updates du workflow
        async for update in stream_workflow_updates(workflow_id):
            await websocket.send_json(update)
    except WebSocketDisconnect:
        print(f"Client disconnected from workflow {workflow_id}")
```

## Structure Recommandée pour l'API

```
src/api/
├── __init__.py
├── app.py                 # Application FastAPI principale
├── dependencies.py        # Dépendances réutilisables
├── middleware.py          # Middlewares personnalisés
├── routes/
│   ├── __init__.py
│   ├── workflows.py       # Routes workflows
│   ├── agents.py          # Routes agents
│   └── health.py          # Routes health/monitoring
└── models/
    ├── __init__.py
    ├── requests.py        # Request models
    └── responses.py       # Response models
```

### Exemple de app.py

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api.routes import workflows, agents, health
from src.api.middleware import add_process_time_header
from src.config.database import init_db, close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()

app = FastAPI(
    title="LangGraph Workflows API",
    description="API for orchestrating agentic workflows",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware
app.middleware("http")(add_process_time_header)

# CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["workflows"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
```

### Exemple de routes/workflows.py

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.dependencies import get_db
from src.api.models.requests import WorkflowExecuteRequest
from src.api.models.responses import WorkflowExecuteResponse

router = APIRouter()

@router.post("/execute", response_model=WorkflowExecuteResponse)
async def execute_workflow(
    request: WorkflowExecuteRequest,
    db: AsyncSession = Depends(get_db)
):
    """Execute a workflow."""
    # Logique d'exécution
    return {"workflow_id": request.workflow_id, "status": "processing"}

@router.get("/{workflow_id}", response_model=WorkflowExecuteResponse)
async def get_workflow_status(
    workflow_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get workflow status."""
    # Logique de récupération
    return {"workflow_id": workflow_id, "status": "completed"}
```

## Bonnes Pratiques

### 1. Async par Défaut

- Utiliser `async def` pour toutes les routes qui font des I/O
- Utiliser des clients async (httpx, asyncpg, etc.)
- Éviter les opérations bloquantes dans les routes async

### 2. Validation Stricte

- Toujours définir des Pydantic models pour requests/responses
- Utiliser `Field()` pour ajouter des contraintes
- Ajouter des validators personnalisés si nécessaire

### 3. Documentation

- Ajouter des docstrings à toutes les routes
- Utiliser `summary` et `description` dans les décorateurs
- Documenter les status codes possibles avec `responses`

```python
@app.post(
    "/workflows/execute",
    response_model=WorkflowResult,
    status_code=201,
    summary="Execute a workflow",
    description="Executes a workflow with the given configuration",
    responses={
        404: {"description": "Workflow not found"},
        422: {"description": "Validation error"},
    }
)
async def execute_workflow(input: WorkflowInput):
    """
    Execute a workflow.

    - **workflow_id**: Unique identifier for the workflow
    - **payload**: Input data for the workflow
    - **timeout**: Maximum execution time in seconds
    """
    pass
```

### 4. Gestion des Erreurs

- Créer des exceptions personnalisées
- Utiliser des exception handlers globaux
- Retourner des erreurs structurées avec des détails

### 5. Testing

```python
from fastapi.testclient import TestClient

def test_execute_workflow():
    client = TestClient(app)
    response = client.post(
        "/api/v1/workflows/execute",
        json={"workflow_id": "wf_123", "payload": {}, "timeout": 30}
    )
    assert response.status_code == 201
    assert response.json()["status"] == "processing"
```

## Dépendances Requises

```toml
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
```

## Lancement de l'Application

```bash
# Développement avec reload
uv run uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000

# Production
uv run uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --workers 4
```

## Ressources

- Documentation officielle: https://fastapi.tiangolo.com
- GitHub: https://github.com/tiangolo/fastapi
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Cas d'Usage du Projet

Dans ce boilerplate, FastAPI est utilisé pour:

1. Exposer des endpoints pour déclencher des workflows
2. Monitorer l'état des agents et workflows
3. Gérer les webhooks d'intégrations externes
4. Streamer les résultats des workflows en temps réel
5. Fournir une API REST pour l'interface utilisateur
