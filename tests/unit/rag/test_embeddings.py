import pytest
from unittest.mock import patch, MagicMock
from src.rag.embeddings import get_embeddings, get_reranker
from src.config.settings import settings

def test_get_embeddings_config():
    """Test if embeddings are initialized with correct model and API key."""
    with patch("src.rag.embeddings.GoogleGenerativeAIEmbeddings") as mock_genai:
        get_embeddings()
        mock_genai.assert_called_once_with(
            model=settings.GOOGLE_EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY
        )

def test_get_reranker_config():
    """Test if reranker is initialized with correct model and API key."""
    with patch("src.rag.embeddings.CohereRerank") as mock_cohere:
        get_reranker(top_n=5)
        mock_cohere.assert_called_once()
        # Check call arguments
        args, kwargs = mock_cohere.call_args
        assert kwargs["top_n"] == 5
        assert kwargs["cohere_api_key"] == settings.COHERE_API_KEY
