from typing import Dict, Any
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.graphs.state import AgentState
from src.rag.retriever import get_retriever_for_client
from src.rag.embeddings import get_reranker
from src.config.settings import settings

# Initialize LLM for routing and generation
llm = ChatGoogleGenerativeAI(
    model=settings.GOOGLE_MODEL,
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0
)

async def route_query(state: AgentState) -> AgentState:
    """
    Determines the business domain of the query.
    Domains: comptable, transaction, exploitation
    """
    query = state.get("query") or state["messages"][-1].content
    
    prompt = ChatPromptTemplate.from_template(
        "Analyze the following user query and classify it into one of these three domains: "
        "'comptable' (accounting, invoices, taxes), "
        "'transaction' (payments, sales, bank operations), "
        "or 'exploitation' (logistics, inventory, daily operations). "
        "Return ONLY the domain name.\n\nQuery: {query}"
    )
    
    chain = prompt | llm
    response = await chain.ainvoke({"query": query})
    domain = response.content.strip().lower()
    
    # Validation
    if domain not in ["comptable", "transaction", "exploitation"]:
        domain = "exploitation" # Fallback
        
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
    
    retriever = get_retriever_for_client(client_id, domain)
    docs = await retriever.ainvoke(query)
    
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
    # Reranking logic using Cohere
    # Note: langchain-cohere provides a compressor/reranker
    # We will pass docs through the reranker
    
    # Format docs for reranking
    docs = state["retrieved_docs"]
    query = state["query"]
    
    # Cohere Rerank usually expects a list of strings or docs
    # langchain-cohere reranker handles this
    reranked_docs = reranker.compress_documents(docs, query)
    
    return {
        **state,
        "retrieved_docs": list(reranked_docs),
        "current_step": "reranked"
    }

async def generate_answer(state: AgentState) -> AgentState:
    """
    Generates the final answer based on the reranked documents.
    """
    docs = state["retrieved_docs"]
    query = state["query"]
    
    context = "\n\n".join([f"Source {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])
    
    prompt = ChatPromptTemplate.from_template(
        "You are a professional business assistant. Use the following pieces of context to answer the question. "
        "If you don't know the answer based on the context, say that you don't know, don't try to make up an answer. "
        "Keep the answer concise and professional.\n\n"
        "Context:\n{context}\n\n"
        "Question: {query}\n\n"
        "Answer:"
    )
    
    chain = prompt | llm
    response = await chain.ainvoke({"context": context, "query": query})
    
    return {
        **state,
        "final_response": response.content,
        "current_step": "completed",
        "messages": [AIMessage(content=response.content)]
    }