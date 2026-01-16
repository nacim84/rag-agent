# Notion API - Guide Complet

## Vue d'ensemble

L'API Notion permet d'interagir avec vos workspaces Notion de manière programmatique. Vous pouvez créer, lire, mettre à jour des pages et bases de données, gérer les blocs de contenu, et automatiser vos workflows.

## Installation

```bash
uv add notion-client
```

## Configuration

### Obtenir une Clé API

1. Aller sur https://www.notion.so/my-integrations
2. Créer une nouvelle intégration
3. Copier le **Internal Integration Token**
4. Partager vos pages/bases de données avec l'intégration

### Variables d'Environnement

```env
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_VERSION=2022-06-28
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Client Notion

### Initialisation

```python
from notion_client import Client
import os

# Initialiser le client
notion = Client(auth=os.environ["NOTION_API_KEY"])

# Ou avec version spécifique
notion = Client(
    auth=os.environ["NOTION_API_KEY"],
    notion_version="2022-06-28"
)
```

## Bases de Données

### Créer une Base de Données

```python
from notion_client import Client
import os

notion = Client(auth=os.environ["NOTION_TOKEN"])

# Créer une base de données avec différents types de propriétés
new_database = notion.databases.create(
    parent={"type": "page_id", "page_id": "parent-page-id-here"},
    title=[{"type": "text", "text": {"content": "Product Inventory"}}],
    icon={"type": "emoji", "emoji": "📦"},
    properties={
        "Name": {"title": {}},
        "Description": {"rich_text": {}},
        "In stock": {"checkbox": {}},
        "Category": {
            "select": {
                "options": [
                    {"name": "Electronics", "color": "blue"},
                    {"name": "Books", "color": "green"},
                    {"name": "Clothing", "color": "red"}
                ]
            }
        },
        "Price": {"number": {"format": "dollar"}},
        "Last ordered": {"date": {}},
        "Suppliers": {
            "multi_select": {
                "options": [
                    {"name": "Supplier A", "color": "purple"},
                    {"name": "Supplier B", "color": "pink"}
                ]
            }
        },
        "Responsible": {"people": {}},
        "Images": {"files": {}}
    }
)

print(f"Database created: {new_database['url']}")
print(f"Database ID: {new_database['id']}")
```

### Récupérer une Base de Données

```python
# Récupérer les métadonnées d'une base de données
database = notion.databases.retrieve(database_id="database-id-here")

print(f"Database name: {database['title'][0]['plain_text']}")
print(f"Properties: {list(database['properties'].keys())}")
```

### Requêter une Base de Données

```python
from notion_client import Client, APIResponseError, APIErrorCode
import os

notion = Client(auth=os.environ["NOTION_TOKEN"])

try:
    # Requête avec filtres complexes
    results = notion.databases.query(
        database_id="database-id-here",
        filter={
            "and": [
                {
                    "property": "Price",
                    "number": {"greater_than": 100}
                },
                {
                    "property": "In stock",
                    "checkbox": {"equals": True}
                }
            ]
        },
        sorts=[
            {"property": "Price", "direction": "descending"},
            {"property": "Name", "direction": "ascending"}
        ],
        page_size=50
    )

    for page in results["results"]:
        name = page["properties"]["Name"]["title"][0]["text"]["content"]
        price = page["properties"]["Price"]["number"]
        print(f"Found item: {name} - ${price}")

except APIResponseError as error:
    if error.code == APIErrorCode.ObjectNotFound:
        print("Database not found or not shared with integration")
    elif error.code == APIErrorCode.RateLimited:
        print("Rate limited - please slow down requests")
    else:
        print(f"API Error: {error.code} - {error}")
```

### Filtres Avancés

```python
# Filtre par texte
filter_text = {
    "property": "Name",
    "rich_text": {"contains": "Python"}
}

# Filtre par nombre
filter_number = {
    "property": "Price",
    "number": {"greater_than_or_equal_to": 50}
}

# Filtre par checkbox
filter_checkbox = {
    "property": "Done",
    "checkbox": {"equals": True}
}

# Filtre par select
filter_select = {
    "property": "Status",
    "select": {"equals": "In Progress"}
}

# Filtre par date
filter_date = {
    "property": "Due Date",
    "date": {"on_or_after": "2024-01-01"}
}

# Filtre combiné (AND)
filter_and = {
    "and": [
        {"property": "Status", "select": {"equals": "Active"}},
        {"property": "Priority", "select": {"equals": "High"}}
    ]
}

# Filtre combiné (OR)
filter_or = {
    "or": [
        {"property": "Category", "select": {"equals": "Urgent"}},
        {"property": "Priority", "select": {"equals": "High"}}
    ]
}

# Utiliser le filtre
results = notion.databases.query(
    database_id="database-id",
    filter=filter_and
)
```

## Pages

### Créer une Page dans une Base de Données

```python
from notion_client import Client
import os

notion = Client(auth=os.environ["NOTION_TOKEN"])

# Créer une page avec différents types de propriétés
new_page = notion.pages.create(
    parent={"database_id": "database-id-here"},
    properties={
        "Name": {
            "title": [{"text": {"content": "Python Programming"}}]
        },
        "Category": {
            "select": {"name": "Books"}
        },
        "Price": {
            "number": 49.99
        },
        "In stock": {
            "checkbox": True
        },
        "Tags": {
            "multi_select": [
                {"name": "Programming"},
                {"name": "Python"}
            ]
        },
        "Due Date": {
            "date": {"start": "2024-12-31"}
        },
        "Responsible": {
            "people": [{"id": "user-id-here"}]
        }
    },
    children=[
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "Overview"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "This is a comprehensive guide to Python programming."
                        }
                    }
                ]
            }
        }
    ]
)

print(f"Page created: {new_page['url']}")
print(f"Page ID: {new_page['id']}")
```

### Récupérer et Mettre à Jour une Page

```python
# Récupérer une page
page = notion.pages.retrieve(page_id="page-id-here")
print(f"Page created: {page['created_time']}")
print(f"Last edited: {page['last_edited_time']}")

# Récupérer avec propriétés filtrées
page_filtered = notion.pages.retrieve(
    page_id="page-id-here",
    filter_properties=["Name", "Price"]
)

# Mettre à jour les propriétés d'une page
updated_page = notion.pages.update(
    page_id="page-id-here",
    properties={
        "Price": {"number": 59.99},
        "In stock": {"checkbox": False},
        "Tags": {
            "multi_select": [
                {"name": "Programming"},
                {"name": "Python"},
                {"name": "Advanced"}
            ]
        }
    },
    icon={"type": "emoji", "emoji": "📚"},
    archived=False
)

print(f"Page updated: {updated_page['url']}")
```

### Archiver une Page

```python
# Archiver (soft delete)
archived_page = notion.pages.update(
    page_id="page-id-here",
    archived=True
)

# Restaurer
restored_page = notion.pages.update(
    page_id="page-id-here",
    archived=False
)
```

## Blocs de Contenu

### Récupérer les Blocs d'une Page

```python
# Récupérer tous les blocs enfants d'une page
blocks = notion.blocks.children.list(block_id="page-id-here")

for block in blocks["results"]:
    block_type = block["type"]
    print(f"Block type: {block_type}")

    # Accéder au contenu selon le type
    if block_type == "paragraph":
        text = block["paragraph"]["rich_text"][0]["plain_text"]
        print(f"Paragraph: {text}")
    elif block_type == "heading_1":
        text = block["heading_1"]["rich_text"][0]["plain_text"]
        print(f"Heading: {text}")
```

### Ajouter des Blocs

```python
# Ajouter des blocs à une page
new_blocks = notion.blocks.children.append(
    block_id="page-id-here",
    children=[
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"text": {"content": "New Section"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "text": {
                            "content": "This is a paragraph with ",
                        }
                    },
                    {
                        "text": {
                            "content": "bold text",
                        },
                        "annotations": {"bold": True}
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"text": {"content": "First item"}}]
            }
        },
        {
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [{"text": {"content": "print('Hello World')"}}],
                "language": "python"
            }
        }
    ]
)
```

## Recherche

### Rechercher dans Notion

```python
# Recherche globale
results = notion.search(
    query="Python",
    filter={
        "property": "object",
        "value": "page"
    },
    sort={
        "direction": "descending",
        "timestamp": "last_edited_time"
    }
)

for result in results["results"]:
    if result["object"] == "page":
        title = result["properties"]["title"]["title"][0]["plain_text"]
        print(f"Found page: {title}")

# Rechercher seulement dans les bases de données
db_results = notion.search(
    query="Tasks",
    filter={
        "property": "object",
        "value": "database"
    }
)
```

## Tools LangChain

### Intégration avec LangChain

```python
from langchain_core.tools import tool
from notion_client import Client
import os

notion = Client(auth=os.environ["NOTION_API_KEY"])

@tool
def create_notion_task(
    database_id: str,
    title: str,
    description: str = None,
    priority: str = "Medium"
) -> dict:
    """Crée une tâche dans une base de données Notion.

    Args:
        database_id: ID de la base de données
        title: Titre de la tâche
        description: Description optionnelle
        priority: Priorité (Low, Medium, High)

    Returns:
        Page créée
    """
    properties = {
        "Name": {"title": [{"text": {"content": title}}]},
        "Status": {"select": {"name": "To Do"}},
        "Priority": {"select": {"name": priority}}
    }

    children = []
    if description:
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"text": {"content": description}}]
            }
        })

    page = notion.pages.create(
        parent={"database_id": database_id},
        properties=properties,
        children=children if children else None
    )

    return {
        "id": page["id"],
        "url": page["url"],
        "title": title
    }

@tool
def query_notion_tasks(
    database_id: str,
    status: str = None,
    priority: str = None
) -> list:
    """Requête des tâches dans Notion.

    Args:
        database_id: ID de la base de données
        status: Filtrer par statut (optionnel)
        priority: Filtrer par priorité (optionnel)

    Returns:
        Liste des tâches trouvées
    """
    filters = []

    if status:
        filters.append({
            "property": "Status",
            "select": {"equals": status}
        })

    if priority:
        filters.append({
            "property": "Priority",
            "select": {"equals": priority}
        })

    filter_obj = {"and": filters} if len(filters) > 1 else filters[0] if filters else None

    results = notion.databases.query(
        database_id=database_id,
        filter=filter_obj
    )

    tasks = []
    for page in results["results"]:
        tasks.append({
            "id": page["id"],
            "title": page["properties"]["Name"]["title"][0]["text"]["content"],
            "status": page["properties"]["Status"]["select"]["name"],
            "url": page["url"]
        })

    return tasks

@tool
def update_notion_task(
    page_id: str,
    status: str = None,
    priority: str = None
) -> dict:
    """Met à jour une tâche Notion.

    Args:
        page_id: ID de la page
        status: Nouveau statut
        priority: Nouvelle priorité

    Returns:
        Page mise à jour
    """
    properties = {}

    if status:
        properties["Status"] = {"select": {"name": status}}

    if priority:
        properties["Priority"] = {"select": {"name": priority}}

    updated = notion.pages.update(
        page_id=page_id,
        properties=properties
    )

    return {
        "id": updated["id"],
        "url": updated["url"]
    }
```

## Bonnes Pratiques

### 1. Gestion des Erreurs

```python
from notion_client import APIResponseError, APIErrorCode

async def safe_notion_query(database_id: str, filter_obj: dict = None):
    """Requête sécurisée avec gestion d'erreur"""
    try:
        results = notion.databases.query(
            database_id=database_id,
            filter=filter_obj
        )
        return {"success": True, "data": results["results"]}

    except APIResponseError as error:
        if error.code == APIErrorCode.ObjectNotFound:
            return {"success": False, "error": "Database not found"}
        elif error.code == APIErrorCode.Unauthorized:
            return {"success": False, "error": "Unauthorized - check API key"}
        elif error.code == APIErrorCode.RateLimited:
            return {"success": False, "error": "Rate limited"}
        else:
            return {"success": False, "error": str(error)}

    except Exception as e:
        return {"success": False, "error": str(e)}
```

### 2. Pagination

```python
def get_all_database_pages(database_id: str) -> list:
    """Récupère toutes les pages avec pagination"""
    all_pages = []
    has_more = True
    start_cursor = None

    while has_more:
        response = notion.databases.query(
            database_id=database_id,
            start_cursor=start_cursor,
            page_size=100
        )

        all_pages.extend(response["results"])
        has_more = response["has_more"]
        start_cursor = response.get("next_cursor")

    return all_pages
```

### 3. Rich Text Helpers

```python
def create_rich_text(text: str, bold: bool = False, italic: bool = False) -> dict:
    """Crée un objet rich text"""
    return {
        "type": "text",
        "text": {"content": text},
        "annotations": {
            "bold": bold,
            "italic": italic
        }
    }

def create_link_text(text: str, url: str) -> dict:
    """Crée un lien dans rich text"""
    return {
        "type": "text",
        "text": {
            "content": text,
            "link": {"url": url}
        }
    }
```

## Limites et Quotas

- **Rate limit**: 3 requêtes par seconde
- **Pagination**: 100 résultats max par requête
- **Taille des blocs**: Limité à 2000 blocs par page
- **Taille du contenu**: Limité à 100 Ko par bloc

## Ressources

- Documentation officielle: https://developers.notion.com
- API Reference: https://developers.notion.com/reference
- SDK Python: https://github.com/ramnes/notion-sdk-py
- Exemples: https://github.com/ramnes/notion-sdk-py/wiki/Examples

## Cas d'Usage du Projet

Dans ce boilerplate, Notion est utilisé pour:

1. Gestion de tâches et projets automatisée
2. Documentation automatique des workflows
3. Logging structuré des exécutions
4. Création de rapports dans des pages Notion
5. Synchronisation de données entre systèmes
6. Base de connaissances pour les agents LangChain
