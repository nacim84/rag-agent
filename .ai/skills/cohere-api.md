# Cohere API - Guide Complet

## Vue d'ensemble

Cohere fournit des modèles de langage de pointe et des APIs pour le traitement du langage naturel. Les principales fonctionnalités incluent : chat, génération de texte, embeddings, reranking et classification.

## Installation

```bash
uv add cohere langchain-cohere
```

## Configuration

### Variables d'Environnement

```env
COHERE_API_KEY=your-api-key-here
COHERE_MODEL=command-r-plus
COHERE_EMBED_MODEL=embed-english-v3.0
COHERE_RERANK_MODEL=rerank-english-v3.0
```

### Initialisation du Client

```python
from cohere import Client

client = Client(
    api_key="YOUR_API_KEY",
    client_name="my-app"  # Optionnel mais recommandé
)
```

## Chat

### Chat Basique

```python
from cohere import Client

client = Client(api_key="YOUR_API_KEY")

# Simple chat
response = client.chat(
    message="What is Python?",
    model="command-r-plus"
)

print(response.text)
```

### Chat avec Historique

```python
# Conversation avec historique
chat_history = [
    {"role": "USER", "message": "Hello, how are you?"},
    {"role": "CHATBOT", "message": "I'm doing well, thank you! How can I help you today?"}
]

response = client.chat(
    message="Can you explain machine learning?",
    chat_history=chat_history,
    model="command-r-plus"
)

print(response.text)

# Ajouter à l'historique
chat_history.append({"role": "USER", "message": "Can you explain machine learning?"})
chat_history.append({"role": "CHATBOT", "message": response.text})
```

### Chat Streaming

```python
from cohere import Client

client = Client(api_key="YOUR_API_KEY")

# Streaming pour réponses en temps réel
response = client.chat_stream(
    message="Write a poem about AI",
    model="command-r-plus"
)

for event in response:
    if event.event_type == "text-generation":
        print(event.text, end="", flush=True)
```

### Chat V2 API (Nouvelle Version)

```python
from cohere import Client, ToolChatMessageV2

client = Client(api_key="YOUR_API_KEY")

# Chat avec V2 API
response = client.v2.chat(
    model="command-r-plus",
    messages=[
        {"role": "user", "content": "Hello, what can you do?"}
    ]
)

print(response.message.content[0].text)

# Streaming V2
response_stream = client.v2.chat_stream(
    model="command-r-plus",
    messages=[
        {"role": "user", "content": "Tell me a story"}
    ]
)

for chunk in response_stream:
    if hasattr(chunk, "delta") and hasattr(chunk.delta, "message"):
        if chunk.delta.message.content:
            print(chunk.delta.message.content.text, end="", flush=True)
```

## Embeddings

### Générer des Embeddings

```python
# Embeddings pour la recherche sémantique
texts = [
    "Python is a programming language",
    "Machine learning is a subset of AI",
    "Deep learning uses neural networks"
]

response = client.embed(
    texts=texts,
    model="embed-english-v3.0",
    input_type="search_document"  # ou "search_query", "classification", "clustering"
)

embeddings = response.embeddings
print(f"Generated {len(embeddings)} embeddings")
print(f"Embedding dimension: {len(embeddings[0])}")
```

### Recherche Sémantique

```python
import numpy as np

# Documents à indexer
documents = [
    "Python is a versatile programming language",
    "JavaScript is used for web development",
    "Machine learning models require training data",
    "Neural networks are inspired by the brain"
]

# Générer embeddings pour les documents
doc_response = client.embed(
    texts=documents,
    model="embed-english-v3.0",
    input_type="search_document"
)
doc_embeddings = np.array(doc_response.embeddings)

# Query embedding
query = "What is Python?"
query_response = client.embed(
    texts=[query],
    model="embed-english-v3.0",
    input_type="search_query"
)
query_embedding = np.array(query_response.embeddings[0])

# Calculer la similarité cosine
similarities = np.dot(doc_embeddings, query_embedding) / (
    np.linalg.norm(doc_embeddings, axis=1) * np.linalg.norm(query_embedding)
)

# Trier par similarité
top_indices = np.argsort(similarities)[::-1]

print("Top results:")
for i in top_indices[:3]:
    print(f"- {documents[i]} (score: {similarities[i]:.3f})")
```

## Reranking

### Reranker des Documents

```python
# Documents à reranker
documents = [
    "Python is a high-level programming language",
    "The Python programming language was created by Guido van Rossum",
    "Java is an object-oriented programming language",
    "Python is widely used in data science and machine learning",
    "JavaScript is the language of the web"
]

# Requête
query = "What is Python programming language?"

# Rerank
response = client.rerank(
    query=query,
    documents=documents,
    model="rerank-english-v3.0",
    top_n=3
)

# Afficher les résultats rerankés
for result in response.results:
    print(f"Rank {result.index + 1}: {documents[result.index]}")
    print(f"Score: {result.relevance_score:.4f}\n")
```

### Reranking avec LangChain

```python
from langchain_cohere import CohereRerank
from langchain.retrievers import ContextualCompressionRetriever

# Créer le reranker
reranker = CohereRerank(
    cohere_api_key="YOUR_API_KEY",
    model="rerank-english-v3.0",
    top_n=5
)

# Utiliser avec un retriever existant
compression_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=your_base_retriever
)

# Utiliser le retriever
results = compression_retriever.get_relevant_documents("Your query here")
```

## Classification

### Classifier du Texte

```python
# Exemples d'entraînement
examples = [
    {"text": "I love this product!", "label": "positive"},
    {"text": "This is terrible", "label": "negative"},
    {"text": "Best purchase ever", "label": "positive"},
    {"text": "Waste of money", "label": "negative"},
    {"text": "Highly recommend", "label": "positive"},
    {"text": "Very disappointed", "label": "negative"}
]

# Textes à classifier
inputs = [
    "This is amazing!",
    "Not worth it",
    "Great value for money"
]

# Classifier
response = client.classify(
    inputs=inputs,
    examples=examples
)

# Afficher les prédictions
for classification in response.classifications:
    print(f"Text: {classification.input}")
    print(f"Prediction: {classification.prediction}")
    print(f"Confidence: {classification.confidence:.2%}\n")
```

## Génération de Texte (Legacy)

### Generate (Deprecated - Utiliser Chat à la place)

```python
# Note: Cette API est deprecated, utilisez chat() à la place

response = client.generate(
    prompt="Write a short story about AI:",
    max_tokens=200,
    temperature=0.7,
    stop_sequences=["---"]
)

print(response.generations[0].text)

# Streaming (deprecated)
response_stream = client.generate_stream(
    prompt="Please explain to me how LLMs work"
)

for chunk in response_stream:
    print(chunk.text, end="", flush=True)
```

## Tools LangChain

### Intégration avec LangChain

```python
from langchain_core.tools import tool
from langchain_cohere import ChatCohere, CohereEmbeddings
import cohere

# LLM Cohere avec LangChain
llm = ChatCohere(
    cohere_api_key="YOUR_API_KEY",
    model="command-r-plus",
    temperature=0.7
)

# Embeddings Cohere avec LangChain
embeddings = CohereEmbeddings(
    cohere_api_key="YOUR_API_KEY",
    model="embed-english-v3.0"
)

# Tool personnalisé pour reranking
@tool
def rerank_documents(
    query: str,
    documents: list[str],
    top_n: int = 5
) -> list[dict]:
    """Reranke des documents avec Cohere.

    Args:
        query: Requête de recherche
        documents: Liste de documents à reranker
        top_n: Nombre de documents à retourner

    Returns:
        Documents rerankés avec scores
    """
    co = cohere.Client("YOUR_API_KEY")

    results = co.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=documents,
        top_n=top_n
    )

    return [
        {
            "index": r.index,
            "document": documents[r.index],
            "relevance_score": r.relevance_score
        }
        for r in results.results
    ]

# Tool pour embeddings
@tool
def get_semantic_embedding(text: str) -> list[float]:
    """Génère un embedding sémantique pour un texte.

    Args:
        text: Texte à embedder

    Returns:
        Vecteur d'embedding
    """
    co = cohere.Client("YOUR_API_KEY")

    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_query"
    )

    return response.embeddings[0]
```

## Cas d'Usage Avancés

### RAG (Retrieval-Augmented Generation)

```python
from langchain_cohere import ChatCohere, CohereEmbeddings, CohereRerank
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import ContextualCompressionRetriever

# 1. Préparer les documents
documents = [
    "Python is a high-level programming language...",
    "Machine learning is a subset of artificial intelligence...",
    # ... plus de documents
]

# 2. Splitter les documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
splits = text_splitter.create_documents(documents)

# 3. Créer le vector store avec Cohere embeddings
embeddings = CohereEmbeddings(model="embed-english-v3.0")
vectorstore = FAISS.from_documents(splits, embeddings)

# 4. Créer le retriever avec reranking
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
reranker = CohereRerank(model="rerank-english-v3.0", top_n=3)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=base_retriever
)

# 5. Utiliser avec le LLM Cohere
llm = ChatCohere(model="command-r-plus")

# 6. Query
query = "What is Python?"
docs = compression_retriever.get_relevant_documents(query)

# 7. Générer la réponse
context = "\n".join([doc.page_content for doc in docs])
response = llm.invoke(f"Context: {context}\n\nQuestion: {query}")

print(response.content)
```

### Classification Multi-Classes

```python
# Définir les catégories
categories = ["technology", "sports", "politics", "entertainment", "science"]

# Exemples par catégorie
examples = []
for category in categories:
    # Ajouter vos exemples ici
    examples.extend([
        {"text": f"Sample text about {category}", "label": category}
        for _ in range(5)
    ])

# Classifier de nouveaux textes
new_texts = [
    "New AI model released by OpenAI",
    "Football team wins championship",
    "Election results announced"
]

response = client.classify(
    inputs=new_texts,
    examples=examples
)

for classification in response.classifications:
    print(f"Text: {classification.input}")
    print(f"Category: {classification.prediction}")
    print(f"Confidence: {classification.confidence:.2%}\n")
```

## Bonnes Pratiques

### 1. Gestion des Erreurs

```python
from cohere.errors import CohereAPIError, CohereConnectionError

def safe_chat(message: str, model: str = "command-r-plus"):
    """Chat avec gestion d'erreur"""
    try:
        response = client.chat(
            message=message,
            model=model
        )
        return {"success": True, "text": response.text}

    except CohereAPIError as e:
        return {"success": False, "error": f"API Error: {e}"}

    except CohereConnectionError as e:
        return {"success": False, "error": f"Connection Error: {e}"}

    except Exception as e:
        return {"success": False, "error": str(e)}
```

### 2. Rate Limiting

```python
from asyncio import Semaphore
import asyncio

# Limiter les requêtes concurrentes
cohere_semaphore = Semaphore(5)

async def rate_limited_embed(texts: list[str]):
    async with cohere_semaphore:
        return client.embed(
            texts=texts,
            model="embed-english-v3.0"
        )
```

### 3. Batch Processing

```python
def batch_embed(texts: list[str], batch_size: int = 96):
    """Embed par batches (max 96 par requête)"""
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = client.embed(
            texts=batch,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        all_embeddings.extend(response.embeddings)

    return all_embeddings
```

### 4. Monitoring des Tokens

```python
# Suivre l'utilisation des tokens
response = client.chat(
    message="Explain quantum computing",
    model="command-r-plus"
)

print(f"Tokens used: {response.meta.tokens}")
print(f"Billed units: {response.meta.billed_units}")
```

## Modèles Disponibles

### Chat Models
- `command-r-plus` - Modèle le plus puissant
- `command-r` - Bon équilibre performance/coût
- `command` - Modèle de base
- `command-light` - Rapide et économique

### Embed Models
- `embed-english-v3.0` - Anglais (dernière version)
- `embed-multilingual-v3.0` - Multi-langue
- `embed-english-light-v3.0` - Version légère

### Rerank Models
- `rerank-english-v3.0` - Anglais
- `rerank-multilingual-v3.0` - Multi-langue

## Limites et Quotas

- **Rate limits**: Varient selon le plan
- **Batch size embeddings**: Max 96 textes
- **Max tokens chat**: Variable selon le modèle
- **Context window**: 128k tokens pour command-r-plus

## Ressources

- Documentation officielle: https://docs.cohere.com
- API Reference: https://docs.cohere.com/reference/
- Python SDK: https://github.com/cohere-ai/cohere-python
- LangChain Integration: https://python.langchain.com/docs/integrations/providers/cohere

## Cas d'Usage du Projet

Dans ce boilerplate, Cohere est utilisé pour:

1. **Reranking** - Améliorer la pertinence des résultats de recherche
2. **Embeddings** - Recherche sémantique dans les documents
3. **Chat** - Alternative aux modèles OpenAI/Anthropic
4. **Classification** - Catégorisation automatique de contenu
5. **RAG** - Augmentation de génération avec retrieval
6. **Semantic Search** - Recherche intelligente dans les données
