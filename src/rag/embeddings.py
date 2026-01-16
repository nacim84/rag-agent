from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_cohere import CohereRerank
from src.config.settings import settings

def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    """
    Returns the Google Gemini embeddings model.
    Must match text-embedding-004 as used in n8n for compatibility.
    """
    return GoogleGenerativeAIEmbeddings(
        model=settings.GOOGLE_EMBEDDING_MODEL,
        google_api_key=settings.GOOGLE_API_KEY
    )

def get_reranker(top_n: int = 4) -> CohereRerank:
    """
    Returns the Cohere Reranker model.
    Standard top_n is 4 as per requirements.
    """
    return CohereRerank(
        model=settings.COHERE_RERANK_MODEL if hasattr(settings, "COHERE_RERANK_MODEL") else "rerank-english-v3.0",
        cohere_api_key=settings.COHERE_API_KEY,
        top_n=top_n
    )
