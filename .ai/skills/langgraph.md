# LangGraph - Compétences et Bonnes Pratiques

## Vue d'ensemble

LangGraph est un framework d'orchestration de bas niveau pour construire, gérer et déployer des agents stateful et des workflows de longue durée. Il fournit une exécution durable, des capacités human-in-the-loop, et une mémoire complète pour les interactions d'agents.

## Concepts Clés

### 1. StateGraph

Le `StateGraph` est le composant central de LangGraph. Il définit comment l'état circule à travers les différents nœuds du graphe.

**Création d'un StateGraph basique:**

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class AgentState(TypedDict):
    """État partagé du graphe."""
    messages: Annotated[List[BaseMessage], add_messages]
    current_step: str
    context: dict
    error: Optional[str]

# Créer le graphe
workflow = StateGraph(AgentState)

# Ajouter des nœuds
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Définir le point d'entrée
workflow.set_entry_point("agent")

# Compiler le graphe avec checkpointer
app = workflow.compile(checkpointer=MemorySaver())
```

### 2. Nœuds (Nodes)

Les nœuds sont des fonctions qui traitent l'état et retournent un nouvel état.

**Définition de nœuds:**

```python
from langgraph.graph import MessagesState

def call_model(state: MessagesState):
    """Appelle le modèle LLM."""
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

def tool_node(state: MessagesState):
    """Exécute les outils."""
    # Logique d'exécution des outils
    return {"messages": tool_results}
```

### 3. Edges (Transitions)

Les edges définissent les transitions entre les nœuds.

**Edges directs:**

```python
# Edge du start vers agent
workflow.add_edge(START, "agent")

# Edge de tools vers agent
workflow.add_edge("tools", "agent")

# Edge vers la fin
workflow.add_edge("agent", END)
```

**Edges conditionnels:**

```python
def should_continue(state: MessagesState) -> str:
    """Détermine la prochaine étape."""
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "tools"
    return END

# Ajouter un edge conditionnel
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)
```

### 4. Checkpointing et Persistence

LangGraph permet de sauvegarder l'état du graphe pour reprendre l'exécution plus tard.

**In-Memory Checkpointer:**

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)
```

**PostgreSQL Checkpointer:**

```python
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

async def get_checkpointer():
    checkpointer = AsyncPostgresSaver.from_conn_string(
        settings.DATABASE_URL.replace("+asyncpg", "")
    )
    await checkpointer.setup()
    return checkpointer

# Utilisation
checkpointer = await get_checkpointer()
app = workflow.compile(checkpointer=checkpointer)
```

### 5. Configuration et Threads

**Exécution avec thread ID:**

```python
from uuid import uuid4

thread_id = str(uuid4())
config = {"configurable": {"thread_id": thread_id}}

# Invoquer le graphe
result = await app.ainvoke(initial_state, config)

# Continuer la conversation avec le même thread
result = await app.ainvoke(new_state, config)
```

## Patterns Avancés

### 1. Agent Tool-Calling ReAct

```python
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END

# Définir les outils
def get_weather(location: str):
    """Get the current weather."""
    if location.lower() in ["sf", "san francisco"]:
        return "It's 60 degrees and foggy."
    else:
        return "It's 90 degrees and sunny."

tool_node = ToolNode([get_weather])

# Créer le modèle avec outils
model = init_chat_model(model="claude-3-5-haiku-latest")
model_with_tools = model.bind_tools([get_weather])

# Fonction de décision
def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

# Fonction de call du modèle
def call_model(state: MessagesState):
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

# Construire le graphe
builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_node("tools", tool_node)
builder.add_edge(START, "call_model")
builder.add_conditional_edges("call_model", should_continue, ["tools", END])
builder.add_edge("tools", "call_model")

graph = builder.compile()
```

### 2. Multi-Agent avec Handoffs

```python
from typing import Literal
from langgraph.graph import StateGraph, START, END

class MultiAgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    next_agent: str

def router(state: MultiAgentState) -> Literal["agent_a", "agent_b", END]:
    """Route vers le bon agent."""
    if state.get("next_agent") == "agent_a":
        return "agent_a"
    elif state.get("next_agent") == "agent_b":
        return "agent_b"
    return END

def agent_a(state: MultiAgentState):
    """Agent spécialisé A."""
    # Logique de l'agent A
    return {"messages": [response], "next_agent": "agent_b"}

def agent_b(state: MultiAgentState):
    """Agent spécialisé B."""
    # Logique de l'agent B
    return {"messages": [response], "next_agent": END}

# Construire le graphe multi-agent
builder = StateGraph(MultiAgentState)
builder.add_node("agent_a", agent_a)
builder.add_node("agent_b", agent_b)
builder.add_edge(START, "agent_a")
builder.add_conditional_edges("agent_a", router)
builder.add_conditional_edges("agent_b", router)

graph = builder.compile(checkpointer=checkpointer)
```

### 3. Workflow avec Boucles

```python
def too_long(state: AgentState) -> bool:
    """Vérifie si le scratchpad est trop long."""
    return len(state["scratchpad"]) > 5

def agent(state: AgentState):
    """Agent qui boucle."""
    return {
        "scratchpad": state["scratchpad"] + [f"Processed: {state['input']}"]
    }

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent)

# Boucle conditionnelle
workflow.add_conditional_edges(
    "agent",
    lambda state: "agent" if not too_long(state) else END,
    {"agent": "agent", END: END}
)

workflow.set_entry_point("agent")
app = workflow.compile(checkpointer=MemorySaver())
```

### 4. Streaming

```python
# Streaming des updates
async def stream_workflow(app, initial_state, config):
    async for chunk in app.astream(initial_state, config, stream_mode="updates"):
        print(f"Update: {chunk}")
        yield chunk

# Streaming des valeurs
async for value in app.astream(initial_state, config, stream_mode="values"):
    print(f"Current state: {value}")
```

## Structure Recommandée

```
src/
├── graphs/
│   ├── __init__.py
│   ├── state.py           # Définitions d'états
│   ├── nodes.py           # Fonctions de nœuds
│   └── edges.py           # Fonctions de conditions
├── agents/
│   └── workflows/
│       ├── __init__.py
│       └── example_workflow.py  # Graphes compilés
```

### Exemple de state.py

```python
from typing import TypedDict, Annotated, List, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """État partagé du graphe."""
    messages: Annotated[List[BaseMessage], add_messages]
    current_step: str
    context: dict
    error: Optional[str]
    final_output: Optional[dict]
```

### Exemple de nodes.py

```python
async def analyze_input(state: AgentState) -> AgentState:
    """Nœud d'analyse de l'entrée."""
    return {
        **state,
        "current_step": "analyzed",
        "context": {"analyzed": True}
    }

async def process_task(state: AgentState) -> AgentState:
    """Nœud de traitement principal."""
    return {
        **state,
        "current_step": "processed"
    }
```

### Exemple de edges.py

```python
def should_continue(state: AgentState) -> str:
    """Détermine la prochaine étape."""
    if state.get("error"):
        return "error_handler"
    if state["current_step"] == "analyzed":
        return "process"
    return END
```

## Bonnes Pratiques

### 1. Gestion de l'État

- Utiliser `TypedDict` pour définir les états
- Utiliser `Annotated` avec `add_messages` pour les listes de messages
- Garder l'état minimal et pertinent
- Documenter chaque champ de l'état

### 2. Nœuds

- Chaque nœud doit être une fonction pure (pas d'effets de bord)
- Retourner seulement les champs d'état qui ont changé
- Gérer les erreurs localement dans chaque nœud
- Ajouter des logs pour le debugging

### 3. Edges Conditionnels

- Garder la logique de routage simple
- Documenter les conditions de transition
- Toujours gérer tous les cas possibles
- Utiliser des types littéraux pour les valeurs de retour

### 4. Checkpointing

- Utiliser PostgreSQL checkpointer en production
- Nettoyer régulièrement les vieux checkpoints
- Inclure des métadonnées utiles dans les configs
- Tester la reprise après crash

### 5. Testing

```python
import pytest
from langchain_core.messages import HumanMessage

@pytest.mark.asyncio
async def test_workflow():
    initial_state = {
        "messages": [HumanMessage(content="Test")],
        "current_step": "start",
        "context": {},
        "error": None,
    }

    result = await app.ainvoke(initial_state, config)

    assert result["current_step"] == "completed"
    assert result["error"] is None
```

## Dépendances Requises

```toml
langgraph>=0.2.0
langgraph-checkpoint-postgres>=0.1.0
langchain-core>=0.3.0
```

## Ressources

- Documentation officielle: https://langchain-ai.github.io/langgraph/
- GitHub: https://github.com/langchain-ai/langgraph
- Exemples: https://github.com/langchain-ai/langgraph/tree/main/examples

## Cas d'Usage du Projet

Dans ce boilerplate, LangGraph est utilisé pour:

1. Orchestrer des workflows multi-étapes complexes
2. Gérer l'état des agents de manière persistante
3. Implémenter des patterns ReAct avec tool calling
4. Créer des systèmes multi-agents avec handoffs
5. Assurer la reprise après crash avec checkpointing
6. Implémenter des boucles de rétroaction et validation
