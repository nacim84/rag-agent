from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from src.config.settings import settings

# 1. SQLAlchemy Engine (for ORM usage like Vector Store)
# We handle the +asyncpg replacement explicitly if needed, but usually settings.DATABASE_URL
# should be compatible or configured separately. Assuming settings.DATABASE_URL is set for asyncpg.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 2. Low-level Connection Pool for LangGraph Checkpointer
_connection_pool: Optional[AsyncConnectionPool] = None

async def init_db_connection():
    """
    Initialize the DB connection pool and LangGraph checkpointer tables.
    Call this on application startup.
    """
    global _connection_pool
    
    # Checkpointer needs a pure psycopg connection string (no +asyncpg)
    conn_string = settings.DATABASE_URL.replace("+asyncpg", "").replace("+psycopg", "")
    
    # Create the pool
    _connection_pool = AsyncConnectionPool(
        conninfo=conn_string,
        min_size=1,
        max_size=10,
        kwargs={"autocommit": True}
    )
    await _connection_pool.open()
    
    # Initialize checkpointer tables once
    async with _connection_pool.connection() as conn:
        checkpointer = AsyncPostgresSaver(conn)
        await checkpointer.setup()
        
    print("✅ Database connection pool and checkpointer initialized.")

async def close_db_connection():
    """Close the DB connection pool."""
    global _connection_pool
    if _connection_pool:
        await _connection_pool.close()
        print("🛑 Database connection pool closed.")

async def get_checkpointer() -> AsyncPostgresSaver:
    """
    Returns a checkpointer instance using the shared connection pool.
    """
    global _connection_pool
    if _connection_pool is None:
        # Fallback for scripts/tests not using lifespan
        await init_db_connection()
        
    # AsyncPostgresSaver is lightweight, it just wraps the connection/pool
    return AsyncPostgresSaver(_connection_pool)