from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from src.api.app import app
from langchain_core.documents import Document

client = TestClient(app)

@patch("src.api.routes.ingest.PGVector")
@patch("src.api.routes.ingest.get_embeddings")
@patch("src.api.routes.ingest.PyPDFLoader")
def test_ingest_pdf_success(mock_loader_cls, mock_get_embeddings, mock_pgvector_cls):
    """
    Test PDF ingestion flow.
    Mocks PDF loading and Vector Store insertion.
    """
    
    # 1. Mock PDF Loader
    mock_loader = AsyncMock()
    mock_loader.aload.return_value = [
        Document(page_content="Page 1 content", metadata={"page": 1}),
        Document(page_content="Page 2 content", metadata={"page": 2})
    ]
    mock_loader_cls.return_value = mock_loader
    
    # 2. Mock Vector Store
    mock_vector_store = AsyncMock()
    mock_pgvector_cls.return_value = mock_vector_store
    
    # 3. Create Dummy PDF file
    files = {
        "file": ("test.pdf", b"%PDF-1.4...", "application/pdf")
    }
    
    # 4. Execute Request
    response = client.post(
        "/api/v1/ingest",
        files=files,
        data={"domain": "comptable"},
        headers={"X-API-Key": "sk_clientA_secret"}
    )
    
    # 5. Verify Response
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["filename"] == "test.pdf"
    assert data["chunks"] > 0 # Splitting happened
    assert data["table"] == "documents_comptable_clientA"
    
    # 6. Verify calls
    mock_pgvector_cls.assert_called()
    # Check collection name passed to PGVector
    _, kwargs = mock_pgvector_cls.call_args
    assert kwargs["collection_name"] == "documents_comptable_clientA"
    
    # Check aadd_documents called
    mock_vector_store.aadd_documents.assert_called()
