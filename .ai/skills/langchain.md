# LangChain - Compétences et Bonnes Pratiques

## Vue d'ensemble

LangChain est un framework pour développer des applications alimentées par des modèles de langage (LLM). Il offre des outils et interfaces pour construire des workflows LLM complexes, des agents, et des chaînes de traitement.

## Concepts Clés

### 1. Agents

Les agents LangChain sont des systèmes qui utilisent un LLM pour décider quelles actions entreprendre. Ils peuvent utiliser des outils pour interagir avec l'environnement.

**Création d'un agent basique:**

```python
from langchain.agents import create_agent

agent = create_agent(
    model,
    tools,
    system_prompt=system_prompt,
)
```

**Agent avec middleware et checkpointer:**

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model,
    system_prompt=(
        "You are a SQL query assistant that helps users "
        "write queries against business databases."
    ),
    middleware=[SkillMiddleware()],
    checkpointer=InMemorySaver(),
)
```

### 2. Chaînes (Chains)

Les chaînes permettent de composer plusieurs appels LLM et transformations de données.

**Chaîne avec outils:**

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig, chain

prompt = ChatPromptTemplate(
    [
        ("system", "You are a helpful assistant."),
        ("human", "{user_input}"),
        ("placeholder", "{messages}"),
    ]
)

# Lier les outils au modèle
llm_with_tools = llm.bind_tools([tool], tool_choice=tool.name)

llm_chain = prompt | llm_with_tools


@chain
def tool_chain(user_input: str, config: RunnableConfig):
    input_ = {"user_input": user_input}
    ai_msg = llm_chain.invoke(input_, config=config)
    tool_msgs = tool.batch(ai_msg.tool_calls, config=config)
    return llm_chain.invoke({**input_, "messages": [ai_msg, *tool_msgs]}, config=config)
```

### 3. Outils (Tools)

Les outils permettent aux agents d'interagir avec des APIs externes ou d'effectuer des actions spécifiques.

**Définition d'un outil:**

```python
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b

# Lier les outils au LLM
tools = [add, multiply, divide]
llm_with_tools = llm.bind_tools(tools)
```

### 4. Messages et Prompts

**Templates de prompts:**

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate(
    [
        ("system", "You are a helpful AI assistant."),
        ("human", "{user_input}"),
        ("placeholder", "{messages}"),
    ]
)
```

**Gestion des messages:**

```python
from langchain.messages import SystemMessage, HumanMessage
from langgraph.graph import add_messages

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is the weather today?")
]

# Ajouter des messages
messages = add_messages(messages, new_message)
```

## Bonnes Pratiques

### 1. Structure du Projet

```
src/
├── agents/              # Agents LangChain
│   ├── base.py
│   └── workflows/
├── chains/              # Chaînes réutilisables
│   └── base_chains.py
├── tools/               # Outils personnalisés
│   ├── base.py
│   └── integrations/
├── prompts/             # Templates de prompts
│   └── templates/
└── config/              # Configuration
    └── settings.py
```

### 2. Intégration LLM

**OpenAI:**

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    api_key=settings.OPENAI_API_KEY,
    model=settings.OPENAI_MODEL,
    temperature=0.7
)
```

**Anthropic:**

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(
    api_key=settings.ANTHROPIC_API_KEY,
    model=settings.ANTHROPIC_MODEL
)
```

**Google:**

```python
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    google_api_key=settings.GOOGLE_API_KEY,
    model=settings.GOOGLE_MODEL
)
```

### 3. Gestion de la Mémoire

**In-Memory Checkpointer:**

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
```

**PostgreSQL Checkpointer:**

```python
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

checkpointer = AsyncPostgresSaver.from_conn_string(
    settings.DATABASE_URL.replace("+asyncpg", "")
)
await checkpointer.setup()
```

### 4. Observabilité avec LangSmith

```python
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT
```

### 5. Gestion des Erreurs

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def call_llm_with_retry(messages):
    return await llm.ainvoke(messages)
```

### 6. Streaming

```python
async def stream_response(agent, messages):
    async for chunk in agent.astream(messages):
        print(chunk)
        yield chunk
```

## Patterns Avancés

### 1. Agent ReAct (Reasoning + Acting)

```python
from langchain.agents import create_agent

tools = [search_tool, calculator_tool, database_tool]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

agent = create_agent(
    llm_with_tools,
    tools,
    system_prompt="You are a helpful assistant that reasons step by step."
)
```

### 2. Multi-Tool Execution

```python
@task
def call_tool(tool_call: ToolCall):
    """Exécute un appel d'outil"""
    tool = tools_by_name[tool_call["name"]]
    return tool.invoke(tool_call)

# Exécution parallèle des outils
tool_result_futures = [
    call_tool(tool_call) for tool_call in llm_response.tool_calls
]
tool_results = [fut.result() for fut in tool_result_futures]
```

### 3. Chaining with LCEL (LangChain Expression Language)

```python
from langchain_core.runnables import RunnablePassthrough

chain = (
    RunnablePassthrough.assign(context=retriever)
    | prompt
    | llm
    | output_parser
)
```

## Dépendances Requises

```toml
# Core
langchain>=0.3.0
langchain-core>=0.3.0
langchain-community>=0.3.0

# LLM Providers
langchain-openai>=0.2.0
langchain-anthropic>=0.2.0
langchain-google-genai>=2.0.0
langchain-cohere>=0.3.0

# Observabilité
langsmith>=0.1.0
```

## Ressources

- Documentation officielle: https://docs.langchain.com
- API Reference: https://api.python.langchain.com
- GitHub: https://github.com/langchain-ai/langchain
- LangSmith: https://smith.langchain.com

## Cas d'Usage du Projet

Dans ce boilerplate, LangChain est utilisé pour:

1. Créer des agents intelligents avec tools
2. Orchestrer des workflows complexes
3. Intégrer multiple LLM providers
4. Gérer la mémoire et l'état des conversations
5. Implémenter des chaînes de traitement réutilisables
6. Tracer et observer les exécutions via LangSmith
