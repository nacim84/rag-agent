# PostgreSQL & SQLAlchemy Async - Compétences et Bonnes Pratiques

## Vue d'ensemble

SQLAlchemy est un toolkit de base de données pour Python qui fournit un ORM (Object Relational Mapper) complet et un langage d'expression SQL. La version async avec asyncpg permet des interactions non-bloquantes avec PostgreSQL.

## Concepts Clés

### 1. Configuration Async Engine

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

# Créer un engine async
engine = create_async_engine(
    "postgresql+asyncpg://user:password@hostname/dbname",
    echo=True,              # Log SQL queries
    pool_size=5,           # Taille du pool de connexions
    max_overflow=10,       # Connexions supplémentaires max
    pool_pre_ping=True,    # Vérifier la connexion avant utilisation
)
```

**Configuration complète:**

```python
from sqlalchemy.ext.asyncio import create_async_engine
from src.config.settings import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,  # Recycler les connexions après 1h
)
```

### 2. Déclaration de Modèles

**Modèles avec Mapped et DeclarativeBase:**

```python
from sqlalchemy import ForeignKey, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
import datetime

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all ORM models."""
    pass

class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(primary_key=True)
    workflow_id: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str]
    status: Mapped[str] = mapped_column(default="pending")
    input_data: Mapped[Optional[dict]]
    output_data: Mapped[Optional[dict]]
    error_message: Mapped[Optional[str]]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relation one-to-many
    runs: Mapped[List["WorkflowRun"]] = relationship(back_populates="workflow")

class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    workflow_id: Mapped[int] = mapped_column(ForeignKey("workflows.id"))
    status: Mapped[str]
    started_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    completed_at: Mapped[Optional[datetime.datetime]]

    # Relation many-to-one
    workflow: Mapped["Workflow"] = relationship(back_populates="runs")
```

### 3. AsyncSession et SessionMaker

**Configuration de session factory:**

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

# Créer une session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Ne pas expirer les objets après commit
)

# Utilisation dans une fonction
async def get_db() -> AsyncSession:
    """Dependency injection for database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

**Utilisation de AsyncSession:**

```python
from sqlalchemy.ext.asyncio import AsyncSession

async def run_some_sql(async_session: async_sessionmaker[AsyncSession]) -> None:
    async with async_session() as session:
        # Ajouter des objets
        session.add(Workflow(
            workflow_id="wf_123",
            name="Test Workflow",
            status="pending"
        ))

        # Commit
        await session.commit()
```

### 4. Requêtes (Queries)

**Select basique:**

```python
from sqlalchemy import select

async def get_workflow(session: AsyncSession, workflow_id: str):
    """Get a workflow by ID."""
    stmt = select(Workflow).where(Workflow.workflow_id == workflow_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

# Utilisation
async with AsyncSessionLocal() as session:
    workflow = await get_workflow(session, "wf_123")
```

**Select avec filtres:**

```python
async def get_active_workflows(session: AsyncSession):
    """Get all active workflows."""
    stmt = (
        select(Workflow)
        .where(Workflow.status == "running")
        .order_by(Workflow.created_at.desc())
        .limit(10)
    )
    result = await session.execute(stmt)
    return result.scalars().all()
```

**Select avec jointures:**

```python
async def get_workflow_with_runs(session: AsyncSession, workflow_id: str):
    """Get workflow with all its runs."""
    stmt = (
        select(Workflow)
        .where(Workflow.workflow_id == workflow_id)
        .options(selectinload(Workflow.runs))  # Eager loading
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
```

**Scalars et streaming:**

```python
from sqlalchemy.future import select

async def stream_workflows(session: AsyncSession):
    """Stream workflows for large result sets."""
    stmt = select(Workflow).order_by(Workflow.id)

    # Scalars - récupérer tous les objets
    result = await session.scalars(stmt)
    for workflow in result:
        print(workflow)

    # Stream - curseur côté serveur
    result = await session.stream(stmt)
    async for workflow in result.scalars():
        print(workflow)
```

### 5. Insert, Update, Delete

**Insert:**

```python
async def create_workflow(session: AsyncSession, workflow_data: dict):
    """Create a new workflow."""
    workflow = Workflow(**workflow_data)
    session.add(workflow)
    await session.commit()
    await session.refresh(workflow)  # Recharger depuis la DB
    return workflow
```

**Update:**

```python
async def update_workflow(
    session: AsyncSession,
    workflow_id: str,
    updates: dict
):
    """Update a workflow."""
    stmt = select(Workflow).where(Workflow.workflow_id == workflow_id)
    result = await session.execute(stmt)
    workflow = result.scalar_one_or_none()

    if workflow:
        for key, value in updates.items():
            setattr(workflow, key, value)
        await session.commit()
        await session.refresh(workflow)

    return workflow
```

**Delete:**

```python
async def delete_workflow(session: AsyncSession, workflow_id: str):
    """Delete a workflow."""
    stmt = select(Workflow).where(Workflow.workflow_id == workflow_id)
    result = await session.execute(stmt)
    workflow = result.scalar_one_or_none()

    if workflow:
        await session.delete(workflow)
        await session.commit()
```

### 6. Transactions

```python
async def transfer_workflow_ownership(
    session: AsyncSession,
    workflow_id: str,
    new_owner_id: int
):
    """Transfer workflow ownership in a transaction."""
    async with session.begin():  # Transaction automatique
        # Récupérer le workflow
        stmt = select(Workflow).where(Workflow.workflow_id == workflow_id)
        result = await session.execute(stmt)
        workflow = result.scalar_one()

        # Mettre à jour
        workflow.owner_id = new_owner_id

        # Le commit est automatique si pas d'erreur
```

**Transaction explicite:**

```python
async def complex_operation(session: AsyncSession):
    """Complex operation with explicit transaction control."""
    try:
        async with session.begin():
            # Opérations multiples
            workflow = Workflow(workflow_id="wf_123", name="Test")
            session.add(workflow)

            run = WorkflowRun(workflow_id=workflow.id, status="running")
            session.add(run)

            # Commit automatique si succès
    except Exception as e:
        # Rollback automatique en cas d'erreur
        print(f"Transaction failed: {e}")
        raise
```

### 7. Relations et Lazy Loading

**Eager Loading (Recommandé en async):**

```python
from sqlalchemy.orm import selectinload, joinedload

async def get_workflow_with_relations(session: AsyncSession, workflow_id: str):
    """Get workflow with eager loaded relationships."""
    stmt = (
        select(Workflow)
        .where(Workflow.workflow_id == workflow_id)
        .options(
            selectinload(Workflow.runs),      # Separate SELECT
            joinedload(Workflow.owner)        # JOIN
        )
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
```

**WriteOnlyMapped (pour grandes collections):**

```python
from sqlalchemy.orm import WriteOnlyMapped

class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    # Collection write-only
    runs: WriteOnlyMapped[WorkflowRun] = relationship()

# Utilisation
async def add_runs_to_workflow(session: AsyncSession, workflow: Workflow):
    # Peut être peuplé avec n'importe quel iterable
    workflow.runs = [WorkflowRun(), WorkflowRun()]

    # Pour itérer, faire un SELECT explicite
    async for run in await session.stream(workflow.runs.select()):
        print(run)
```

## Patterns Avancés

### 1. Repository Pattern

```python
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class WorkflowRepository:
    """Repository for Workflow operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, workflow_id: str) -> Optional[Workflow]:
        """Get workflow by ID."""
        stmt = select(Workflow).where(Workflow.workflow_id == workflow_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, limit: int = 100) -> List[Workflow]:
        """Get all workflows."""
        stmt = select(Workflow).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, workflow_data: dict) -> Workflow:
        """Create a new workflow."""
        workflow = Workflow(**workflow_data)
        self.session.add(workflow)
        await self.session.commit()
        await self.session.refresh(workflow)
        return workflow

    async def update(self, workflow_id: str, updates: dict) -> Optional[Workflow]:
        """Update a workflow."""
        workflow = await self.get_by_id(workflow_id)
        if workflow:
            for key, value in updates.items():
                setattr(workflow, key, value)
            await self.session.commit()
            await self.session.refresh(workflow)
        return workflow

    async def delete(self, workflow_id: str) -> bool:
        """Delete a workflow."""
        workflow = await self.get_by_id(workflow_id)
        if workflow:
            await self.session.delete(workflow)
            await self.session.commit()
            return True
        return False
```

### 2. Base Repository

```python
from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar('T', bound=Base)

class BaseRepository(Generic[T]):
    """Generic base repository."""

    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int) -> Optional[T]:
        return await self.session.get(self.model, id)

    async def get_all(self, limit: int = 100) -> List[T]:
        stmt = select(self.model).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, id: int) -> bool:
        obj = await self.get(id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return True
        return False

# Utilisation
workflow_repo = BaseRepository(Workflow, session)
```

### 3. Database Config Module

```python
# src/config/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from src.config.settings import settings

# Engine SQLAlchemy async
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10,
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    """Close database connections."""
    await engine.dispose()

async def get_db() -> AsyncSession:
    """Dependency for database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Checkpointer LangGraph
async def get_checkpointer() -> AsyncPostgresSaver:
    """Get LangGraph PostgreSQL checkpointer."""
    checkpointer = AsyncPostgresSaver.from_conn_string(
        settings.DATABASE_URL.replace("+asyncpg", "")
    )
    await checkpointer.setup()
    return checkpointer
```

## Bonnes Pratiques

### 1. Structure du Projet

```
src/
├── models/
│   ├── __init__.py
│   ├── base.py           # Base et configuration
│   ├── workflow.py       # Modèle Workflow
│   └── user.py           # Modèle User
├── repositories/
│   ├── __init__.py
│   ├── base.py           # BaseRepository
│   └── workflow.py       # WorkflowRepository
└── config/
    └── database.py       # Configuration DB
```

### 2. Migrations avec Alembic

```bash
# Créer une migration
uv run alembic revision --autogenerate -m "Add workflows table"

# Appliquer les migrations
uv run alembic upgrade head

# Revenir en arrière
uv run alembic downgrade -1
```

### 3. Indexes et Performance

```python
from sqlalchemy import Index

class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(primary_key=True)
    workflow_id: Mapped[str] = mapped_column(unique=True, index=True)
    status: Mapped[str] = mapped_column(index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(index=True)

    # Index composite
    __table_args__ = (
        Index('idx_status_created', 'status', 'created_at'),
    )
```

### 4. Testing

```python
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

@pytest.fixture
async def test_db():
    """Create test database."""
    engine = create_async_engine("postgresql+asyncpg://test:test@localhost/test_db")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession)

    yield async_session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

@pytest.mark.asyncio
async def test_create_workflow(test_db):
    async with test_db() as session:
        workflow = Workflow(workflow_id="wf_test", name="Test")
        session.add(workflow)
        await session.commit()

        result = await session.get(Workflow, workflow.id)
        assert result.workflow_id == "wf_test"
```

## Dépendances Requises

```toml
sqlalchemy[asyncio]>=2.0.0
asyncpg>=0.29.0
psycopg[binary]>=3.1.0
alembic>=1.13.0
```

## Ressources

- Documentation SQLAlchemy: https://docs.sqlalchemy.org/en/20/
- Documentation asyncpg: https://magicstack.github.io/asyncpg/
- Tutorial async: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html

## Cas d'Usage du Projet

Dans ce boilerplate, PostgreSQL et SQLAlchemy sont utilisés pour:

1. Stocker les états des workflows LangGraph (checkpointing)
2. Persister les résultats des exécutions
3. Gérer les métadonnées des agents
4. Logger les intégrations API
5. Stocker les configurations et paramètres
6. Gérer les utilisateurs et permissions
