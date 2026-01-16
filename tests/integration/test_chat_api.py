from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from src.api.app import app
from langchain_core.documents import Document

client = TestClient(app)

# We patch the nodes in the workflow definition file because that's where they are imported
@patch("src.agents.workflows.rag_workflow.get_checkpointer", new_callable=AsyncMock)
@patch("src.agents.workflows.rag_workflow.route_query")
@patch("src.agents.workflows.rag_workflow.generate_answer")
@patch("src.graphs.nodes.get_retriever_for_client")
@patch("src.graphs.nodes.get_reranker")
def test_chat_flow_success(mock_get_reranker, mock_get_retriever, mock_generate, mock_route, mock_checkpointer):
    """
    Integration test validating API -> Workflow -> Node Execution -> API Response.
    Mocks complex nodes (LLM calls) but keeps retrieval logic active to verify parameter passing.
    """
    
    # 1. Disable Checkpointer
    mock_checkpointer.return_value = None
    
    # 2. Mock Node Behaviors
    # route_query: update state with domain
    async def mock_route_impl(state):
        return {**state, "domain": "comptable", "current_step": "routed"}
    mock_route.side_effect = mock_route_impl
    
    # generate_answer: update state with final response
    async def mock_generate_impl(state):
        return {
            **state, 
            "final_response": "The answer is 42", 
            "current_step": "completed"
        }
    mock_generate.side_effect = mock_generate_impl
    
    # 3. Mock Retriever (Keep retrieve_docs logic active to test client_id passing)
    mock_retriever = AsyncMock()
    mock_retriever.ainvoke.return_value = [Document(page_content="Doc 1", metadata={"id": 1})]
    mock_get_retriever.return_value = mock_retriever
    
    # 4. Mock Reranker
    mock_rerank_instance = MagicMock()
    # compress_documents returns a list of Documents
    mock_rerank_instance.compress_documents.return_value = [Document(page_content="Doc 1", metadata={"id": 1})]
    mock_get_reranker.return_value = mock_rerank_instance

    # 5. Execute Request
    response = client.post(
        "/api/v1/chat",
        json={"query": "Combien ça coûte ?"},
        headers={"X-API-Key": "sk_clientA_secret123"}
    )
    
    # Debug info if fails
    if response.status_code != 200:
        print(response.json())

    # 6. Verify Response
    assert response.status_code == 200
    data = response.json()
    
    assert data["answer"] == "The answer is 42"
    assert data["domain"] == "comptable"
    assert len(data["sources"]) == 1
    assert data["sources"][0]["content"] == "Doc 1"
    
    # Verify Auth extracted client_id correctly and passed it to retrieval
    mock_get_retriever.assert_called_with("clientA", "comptable")

def test_chat_auth_failure():
    response = client.post(
        "/api/v1/chat",
        json={"query": "Hello"},
        headers={"X-API-Key": "invalid_format"}
    )
    assert response.status_code == 403
