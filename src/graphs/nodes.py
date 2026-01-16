from typing import Dict, Any, List, Union
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.graphs.state import AgentState
from src.rag.retriever import get_retriever_for_client
from src.rag.embeddings import get_reranker
from src.config.settings import settings
from src.config.logging import get_logger

logger = get_logger("agent.nodes")

# Initialize LLM for routing and generation
llm = ChatGoogleGenerativeAI(
    model=settings.GOOGLE_MODEL,
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0
)

def _extract_text_content(message_content: Union[str, List[Union[str, Dict]]]) -> str:
    """Helper to extract text from potential multimodal content."""
    if isinstance(message_content, list):
        return "".join([
            part if isinstance(part, str) else part.get("text", "") 
            for part in message_content
        ])
    return str(message_content)

async def route_query(state: AgentState) -> AgentState:
    """
    Determines the business domain of the query.
    Domains: comptable, transaction, exploitation
    """
    # Use the last message content as query
    last_message = state["messages"][-1]
    query = last_message.content
    # Ensure query is string
    if not isinstance(query, str):
        query = _extract_text_content(query)
    
    prompt = ChatPromptTemplate.from_template(
        "Analyze the following user query and classify it into one of these three domains: "
        "'comptable' (accounting, invoices, taxes), "
        "'transaction' (payments, sales, bank operations), "
        "or 'exploitation' (logistics, inventory, daily operations). "
        "Return ONLY the domain name.\n\nQuery: {query}"
    )
    
    chain = prompt | llm
    response = await chain.ainvoke({"query": query})
    
    # Robust content extraction
    content = _extract_text_content(response.content)
    domain = content.strip().lower()
    
    # Validation
    if domain not in ["comptable", "transaction", "exploitation"]:
        logger.warning("domain_fallback", original_domain=domain, fallback="exploitation")
        domain = "exploitation" # Fallback
    
    logger.info("query_routed", domain=domain, query_snippet=query[:50])
        
    return {
        **state,
        "domain": domain,
        "query": query,
        "current_step": "routed"
    }

async def retrieve_docs(state: AgentState) -> AgentState:
    """
    Retrieves documents from the specific client/domain vector store.
    """
    client_id = state["client_id"]
    domain = state["domain"]
    query = state["query"]
    
    logger.info("retrieving_docs", client_id=client_id, domain=domain)
    
    retriever = get_retriever_for_client(client_id, domain)
    docs = await retriever.ainvoke(query)
    
    logger.info("docs_retrieved", count=len(docs))
    
    return {
        **state,
        "retrieved_docs": docs,
        "current_step": "retrieved"
    }

async def rerank_docs(state: AgentState) -> AgentState:
    """
    Uses Cohere to rerank the retrieved documents for relevance.
    """
    if not state["retrieved_docs"]:
        return {**state, "current_step": "reranked"}
        
    reranker = get_reranker()
    
    docs = state["retrieved_docs"]
    query = state["query"]
    
    reranked_docs = reranker.compress_documents(docs, query)
    
    logger.info("docs_reranked", count=len(list(reranked_docs)), original_count=len(docs))
    
    return {
        **state,
        "retrieved_docs": list(reranked_docs),
        "current_step": "reranked"
    }

async def generate_answer(state: AgentState) -> AgentState:
    """
    Generates the final answer based on the reranked documents and conversation history.
    """
    docs = state["retrieved_docs"]
    
    context = "\n\n".join([f"Source {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional business assistant. Use the following pieces of context to answer the users question. "
                   "If you don't know the answer based on the context, say that you don't know. "
                   "Keep the answer concise and professional.\n\n"
                   "Context:\n{context}"),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    chain = prompt | llm
    
    logger.info("generating_answer", context_length=len(context))
    
    response = await chain.ainvoke({
        "context": context,
        "messages": state["messages"]
    })
    
    content = _extract_text_content(response.content)
    
    return {
        **state,
        "final_response": content,
        "current_step": "completed",
        "messages": [AIMessage(content=content)]
    }
