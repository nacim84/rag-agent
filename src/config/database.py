from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config.settings import settings

# Engine SQLAlchemy async
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10,
)

# Session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Checkpointer LangGraph
async def get_checkpointer() -> AsyncPostgresSaver:
    """Retourne un checkpointer PostgreSQL pour LangGraph."""
    checkpointer = AsyncPostgresSaver.from_conn_string(
        settings.DATABASE_URL.replace("+asyncpg", "")
    )
    await checkpointer.setup()
    return checkpointer
