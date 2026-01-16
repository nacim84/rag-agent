# Pydantic - Compétences et Bonnes Pratiques

## Vue d'ensemble

Pydantic est une bibliothèque de validation de données pour Python qui utilise les annotations de type pour définir des schémas de données. Elle offre une validation rapide et extensible, permettant une sérialisation et désérialisation puissante.

## Concepts Clés

### 1. BaseModel

`BaseModel` est la classe de base pour tous les modèles Pydantic.

```python
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    is_active: bool = True

# Création et validation
user = User(id=1, name="John Doe", email="john@example.com")
print(user.model_dump())  # {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'age': None, 'is_active': True}
```

### 2. Field Validation avec Field()

```python
from pydantic import BaseModel, Field
from typing import Annotated

class WorkflowConfig(BaseModel):
    workflow_id: str = Field(..., min_length=1, max_length=100, pattern=r"^wf_")
    timeout: int = Field(default=30, ge=1, le=300, description="Timeout in seconds")
    max_retries: int = Field(default=3, ge=0, le=10)
    tags: list[str] = Field(default_factory=list, max_length=10)

# Utilisation
config = WorkflowConfig(
    workflow_id="wf_12345",
    timeout=60,
    max_retries=5,
    tags=["production", "high-priority"]
)
```

### 3. Validators

**field_validator - Validation d'un ou plusieurs champs:**

```python
from pydantic import BaseModel, field_validator
from typing import Any

class Model(BaseModel):
    f1: str
    f2: str

    @field_validator('f1', 'f2', mode='before')
    @classmethod
    def capitalize(cls, value: str) -> str:
        """Capitalise les valeurs avant validation."""
        return value.capitalize()

    @field_validator('f1')
    @classmethod
    def ensure_foobar(cls, v: Any):
        """Vérifie que 'foobar' est présent."""
        if 'foobar' not in v:
            raise ValueError('"foobar" not found in f1')
        return v

# Utilisation
model = Model(f1="this is foobar good", f2="hello")
# model.f1 = "This is foobar good"
# model.f2 = "Hello"
```

**model_validator - Validation au niveau du modèle:**

```python
from pydantic import BaseModel, model_validator

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    password_confirm: str

    @model_validator(mode='after')
    def check_passwords_match(self):
        """Vérifie que les mots de passe correspondent."""
        if self.password != self.password_confirm:
            raise ValueError('Passwords do not match')
        return self
```

### 4. Model Config

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,      # Supprime les espaces
        validate_default=True,           # Valide les valeurs par défaut
        validate_assignment=True,        # Valide lors de l'assignation
        extra='forbid',                  # Interdit les champs supplémentaires
        frozen=False,                    # Permet la modification
    )

    name: str
    email: str
```

### 5. model_validate - Validation d'objets

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    name: str
    age: int

# Validation basique
user_data = {"name": "John", "age": 30}
user = User.model_validate(user_data)

# Validation stricte
user = User.model_validate({"name": "John", "age": "30"}, strict=True)

# Gestion des champs supplémentaires
user = User.model_validate(
    {"name": "John", "age": 30, "extra_field": "ignored"},
    extra="ignore"
)

# Depuis les attributs d'un objet
class UserObj:
    name = "John"
    age = 30

user = User.model_validate(UserObj(), from_attributes=True)

# Avec contexte personnalisé
user = User.model_validate(user_data, context={"source": "api"})
```

### 6. Sérialisation

```python
from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    id: int
    name: str
    timestamp: datetime

event = Event(id=1, name="Test Event", timestamp=datetime.now())

# Convertir en dict
data = event.model_dump()

# Convertir en JSON
json_str = event.model_dump_json()

# Exclure certains champs
data = event.model_dump(exclude={'timestamp'})

# Inclure seulement certains champs
data = event.model_dump(include={'id', 'name'})
```

### 7. Pydantic Settings

Pour gérer la configuration de l'application à partir de variables d'environnement.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """Configuration centralisée de l'application."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Application
    APP_NAME: str = "langgraph-workflow"
    APP_ENV: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # LLM Providers
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    # LangSmith
    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_API_KEY: Optional[str] = None

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

# Utilisation
settings = Settings()  # Charge automatiquement depuis .env
```

### 8. Types Avancés

**Annotated Types:**

```python
from pydantic import BaseModel, Field
from typing import Annotated

PositiveInt = Annotated[int, Field(gt=0)]
EmailStr = Annotated[str, Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')]

class User(BaseModel):
    id: PositiveInt
    email: EmailStr
```

**Custom Types:**

```python
from pydantic import BaseModel, field_validator
from typing import NewType

WorkflowId = NewType('WorkflowId', str)

class Workflow(BaseModel):
    id: WorkflowId
    name: str

    @field_validator('id')
    @classmethod
    def validate_workflow_id(cls, v: str) -> str:
        if not v.startswith('wf_'):
            raise ValueError('Workflow ID must start with "wf_"')
        return v
```

**Union Types:**

```python
from pydantic import BaseModel
from typing import Union

class SuccessResponse(BaseModel):
    status: str = "success"
    data: dict

class ErrorResponse(BaseModel):
    status: str = "error"
    error: str
    code: int

Response = Union[SuccessResponse, ErrorResponse]

class APIResponse(BaseModel):
    response: Response
```

## Patterns Avancés

### 1. Nested Models

```python
from pydantic import BaseModel
from typing import List

class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    name: str
    email: str
    addresses: List[Address]

user = User(
    name="John",
    email="john@example.com",
    addresses=[
        {"street": "123 Main St", "city": "New York", "country": "USA"},
        {"street": "456 Oak Ave", "city": "San Francisco", "country": "USA"}
    ]
)
```

### 2. Generic Models

```python
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    data: T
    status: str
    message: str

class User(BaseModel):
    id: int
    name: str

# Utilisation
user_response = Response[User](
    data={"id": 1, "name": "John"},
    status="success",
    message="User retrieved"
)
```

### 3. Validation Conditionnelle

```python
from pydantic import BaseModel, model_validator

class PaymentRequest(BaseModel):
    payment_method: str
    card_number: str | None = None
    bank_account: str | None = None

    @model_validator(mode='after')
    def check_payment_details(self):
        if self.payment_method == "card" and not self.card_number:
            raise ValueError('Card number required for card payments')
        if self.payment_method == "bank" and not self.bank_account:
            raise ValueError('Bank account required for bank payments')
        return self
```

### 4. Computed Fields

```python
from pydantic import BaseModel, computed_field

class User(BaseModel):
    first_name: str
    last_name: str
    age: int

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @computed_field
    @property
    def is_adult(self) -> bool:
        return self.age >= 18
```

## Bonnes Pratiques

### 1. Structure des Modèles

```
src/
├── schemas/
│   ├── __init__.py
│   ├── base.py          # Schémas de base
│   ├── workflow.py      # Schémas workflow
│   ├── agent.py         # Schémas agent
│   └── requests.py      # Schémas de requêtes
```

### 2. Validation Stricte

- Toujours utiliser `Field()` pour ajouter des contraintes
- Utiliser `model_validator` pour les validations inter-champs
- Définir `extra='forbid'` pour rejeter les champs inconnus

### 3. Documentation

```python
from pydantic import BaseModel, Field

class WorkflowConfig(BaseModel):
    """Configuration for a workflow execution.

    This model defines all the parameters needed to execute
    a workflow, including timeout, retries, and metadata.
    """

    workflow_id: str = Field(
        ...,
        description="Unique identifier for the workflow",
        example="wf_12345"
    )
    timeout: int = Field(
        default=30,
        description="Maximum execution time in seconds",
        ge=1,
        le=300
    )
```

### 4. Testing

```python
import pytest
from pydantic import ValidationError

def test_workflow_config_validation():
    # Test valide
    config = WorkflowConfig(workflow_id="wf_123", timeout=60)
    assert config.timeout == 60

    # Test invalid
    with pytest.raises(ValidationError) as exc_info:
        WorkflowConfig(workflow_id="invalid", timeout=-1)

    errors = exc_info.value.errors()
    assert len(errors) == 2
```

### 5. Performance

- Utiliser `model_validate` au lieu de `parse_obj` (deprecated)
- Utiliser `model_dump_json()` au lieu de `json()`
- Désactiver `validate_default` si non nécessaire
- Utiliser `frozen=True` pour les modèles immutables

## Dépendances Requises

```toml
pydantic>=2.0.0
pydantic-settings>=2.0.0
email-validator>=2.0.0  # Pour EmailStr
```

## Ressources

- Documentation officielle: https://docs.pydantic.dev
- GitHub: https://github.com/pydantic/pydantic
- Migration v1 -> v2: https://docs.pydantic.dev/latest/migration/

## Cas d'Usage du Projet

Dans ce boilerplate, Pydantic est utilisé pour:

1. Validation des requêtes API (FastAPI)
2. Configuration de l'application via variables d'environnement
3. Définition des schémas de données pour workflows et agents
4. Sérialisation/désérialisation des états LangGraph
5. Validation des paramètres d'outils LangChain
6. Définition des modèles de réponse structurés
