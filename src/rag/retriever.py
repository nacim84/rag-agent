from langchain_postgres import PGVector
from src.rag.embeddings import get_embeddings
from src.config.settings import settings
from src.config.database import engine # Import shared AsyncEngine

def get_retriever_for_client(client_id: str, domain: str):
    """
    Creates a PGVector retriever for a specific client and domain.
    Table pattern: documents_{domain}_{client_id}
    """
    table_name = f"documents_{domain}_{client_id}"
    embeddings = get_embeddings()
    
    # PGVector from langchain-postgres
    # Fix: Use shared async engine and disable extension creation
    # to avoid asyncpg concurrency issues
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=table_name,
        connection=engine,
        use_jsonb=True,
        create_extension=False,
    )
    
    return vector_store.as_retriever(
        search_kwargs={"k": 10} # Get more chunks before reranking
    )