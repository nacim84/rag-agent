# Workflow EPCT : Evaluate, Plan, Code, Test

Ce workflow est la methode standard pour implementer de nouvelles fonctionnalites ou effectuer des modifications importantes dans le codebase.

**IMPORTANT** : Ce workflow utilise des sub-agents specialises pour economiser le contexte du main agent. Chaque phase delegue le travail a l'agent expert correspondant.

---

## Architecture Multi-Agents EPCT

```
[Main Agent / Supervisor]
        |
        +---> [E] codebase-explorer-expert --> Analyse & Exploration
        |
        +---> [P] langgraph-architect-expert --> Architecture & Plan
        |
        +---> [C] python-developer-expert --> Implementation
        |
        +---> [T] testing-expert --> Tests & Validation
        |
        v
[Resultat Final]
```

---

## Protocole de Contexte Partage

**CRITIQUE** : Avant et apres chaque phase, le contexte partage DOIT etre mis a jour.

- **Fichier** : `.ai/shared-context/session-active.md`
- **Regles** : `.ai/shared-context/rules.md`

Chaque sub-agent :
1. LIT le contexte partage au debut de sa tache
2. MET A JOUR le contexte partage a la fin de sa tache

---

## E - Evaluate (Evaluer)

**Agent** : `codebase-explorer-expert`

### Mission
Comprendre l'existant et l'impact de la modification avant d'ecrire du code.

### Invocation
```
Deleguer a @.ai/agents/codebase-explorer-expert.md

Tache : Evaluer l'impact de [DESCRIPTION DE LA DEMANDE]

Actions requises :
1. Reformuler la demande pour confirmer la comprehension
2. Explorer le codebase pour identifier les fichiers concernes
3. Analyser les dependances (imports, DB, services)
4. Consulter .ai/skills/ et .ai/agents/ pour les patterns
5. Produire un rapport d'impact

Format de sortie attendu : Rapport Quick Scan ou Deep Dive
```

### Output Attendu
```markdown
## Rapport d'Evaluation - [Fonctionnalite]

### Comprehension de la Demande
[Reformulation]

### Fichiers Concernes
| Fichier | Role | Impact |
|---------|------|--------|
| src/... | ... | Haut/Moyen/Bas |

### Dependances Identifiees
- [Liste des modules/services impactes]

### Risques et Points d'Attention
- [Liste]

### Recommandations pour la Phase Plan
- [Liste]
```

---

## P - Plan (Planifier)

**Agent** : `langgraph-architect-expert`

### Mission
Etablir une strategie technique claire et definir l'architecture de la solution.

### Invocation
```
Deleguer a @.ai/agents/langgraph-architect-expert.md

Contexte : [RAPPORT D'EVALUATION de la phase E]

Tache : Planifier l'implementation de [DESCRIPTION]

Actions requises :
1. Definir la strategie technique (nouveaux fichiers, modifications)
2. Choisir le pattern architectural adapte
3. Definir les schemas de donnees (State, Pydantic models)
4. Lister les cas de tests a implementer
5. Produire un plan d'implementation detaille

Format de sortie attendu : Plan d'implementation structure
```

### Output Attendu
```markdown
## Plan d'Implementation - [Fonctionnalite]

### Pattern Architectural Choisi
[Single Agent / Supervisor / Hierarchical / Plan-and-Execute / etc.]

### Modifications Requises

#### Nouveaux Fichiers
| Fichier | Description |
|---------|-------------|
| src/... | ... |

#### Fichiers a Modifier
| Fichier | Modifications |
|---------|---------------|
| src/... | ... |

### Schemas de Donnees
```python
class NewState(TypedDict):
    # Definition
```

### Definition du State/Nodes/Edges (si LangGraph)
- Entry point: ...
- Nodes: [liste]
- Edges: [liste]

### Cas de Tests a Implementer
1. test_... : [description]
2. test_... : [description]

### Ordre d'Implementation
1. [Etape 1]
2. [Etape 2]
3. ...
```

---

## C - Code (Coder)

**Agent** : `python-developer-expert`

### Mission
Implementer la solution en suivant le plan etabli et les conventions du projet.

### Invocation
```
Deleguer a @.ai/agents/python-developer-expert.md

Contexte : [PLAN D'IMPLEMENTATION de la phase P]

Tache : Implementer [DESCRIPTION] selon le plan

Actions requises :
1. Lire le contexte partage pour les decisions precedentes
2. Implementer les fichiers dans l'ordre defini
3. Respecter les patterns LangGraph (State, Nodes, Edges)
4. Utiliser le typage fort (Pydantic/Type Hints)
5. Preferer l'asynchrone (async/await)
6. Ajouter les docstrings Google Style
7. Mettre a jour le contexte partage

Regles :
- Utiliser UNIQUEMENT uv pour les dependances
- Respecter le style snake_case
- Imports structures (stdlib, third-party, local)
```

### Output Attendu
```markdown
## Rapport d'Implementation - [Fonctionnalite]

### Fichiers Crees
| Fichier | Lignes | Description |
|---------|--------|-------------|
| src/... | XX | ... |

### Fichiers Modifies
| Fichier | Modifications |
|---------|---------------|
| src/... | ... |

### Dependances Ajoutees
```bash
uv add [packages]
```

### Points d'Attention pour les Tests
- [Liste des cas critiques a tester]

### Etat : PRET POUR TESTS
```

---

## T - Test (Tester)

**Agent** : `testing-expert`

### Mission
Verifier la qualite et la robustesse de l'implementation.

### Invocation
```
Deleguer a @.ai/agents/testing-expert.md

Contexte : [RAPPORT D'IMPLEMENTATION de la phase C]

Tache : Tester et valider [DESCRIPTION]

Actions requises :
1. Lire le contexte partage
2. Implementer les tests unitaires definis dans le plan
3. Implementer les tests d'integration si necessaire
4. Executer la suite de tests complete
5. Verifier la qualite du code (ruff, mypy)
6. Produire un rapport de tests
7. Mettre a jour le contexte partage

Commandes :
- uv run pytest tests/ -v
- uv run pytest --cov=src
- uv run ruff check src/
- uv run mypy src/
```

### Output Attendu
```markdown
## Rapport de Tests - [Fonctionnalite]

### Resume
| Metrique | Valeur | Objectif | Statut |
|----------|--------|----------|--------|
| Tests passes | X/Y | 100% | PASS/FAIL |
| Couverture | XX% | >= 80% | PASS/FAIL |
| Ruff | 0 erreurs | 0 | PASS/FAIL |
| MyPy | 0 erreurs | 0 | PASS/FAIL |

### Tests Implementes
| Test | Description | Statut |
|------|-------------|--------|
| test_... | ... | PASS/FAIL |

### Bugs Identifies (si echec)
1. [Description + fichier:ligne]

### Verdict Final
- [ ] VALIDE - Pret pour merge
- [ ] ECHEC - Retour phase C ou P necessaire
```

---

## Gestion des Echecs

### Si Phase T echoue

```
1. Analyser le rapport de tests
2. Si bug simple --> Retour Phase C (meme agent)
3. Si probleme architectural --> Retour Phase P
4. Si mauvaise comprehension --> Retour Phase E
```

### Boucle de Correction

```
[T: ECHEC] --> Analyser la cause
    |
    +-- Bug implementation --> [C] python-developer-expert
    |
    +-- Probleme design --> [P] langgraph-architect-expert
    |
    +-- Mauvaise analyse --> [E] codebase-explorer-expert
```

---

## Exemple d'Execution Complete

```markdown
## EPCT : Ajouter un endpoint de recherche RAG

### Phase E - Evaluation
> Deleguer a codebase-explorer-expert
> "Evaluer l'impact d'ajouter un endpoint /search avec RAG"

Resultat : Rapport identifiant src/api/, src/chains/, tests/

### Phase P - Plan
> Deleguer a langgraph-architect-expert
> Contexte : [Rapport E]
> "Planifier l'implementation du endpoint /search"

Resultat : Plan avec schema, route, chain, tests definis

### Phase C - Code
> Deleguer a python-developer-expert
> Contexte : [Plan P]
> "Implementer le endpoint /search selon le plan"

Resultat : Code implemente, 3 fichiers crees, 2 modifies

### Phase T - Test
> Deleguer a testing-expert
> Contexte : [Rapport C]
> "Tester le endpoint /search"

Resultat : 8/8 tests passes, 87% couverture, VALIDE
```

---

## Checklist Main Agent

Avant de lancer EPCT :
- [ ] Demande claire et comprise
- [ ] Contexte partage initialise

Pendant EPCT :
- [ ] Phase E: codebase-explorer-expert invoque
- [ ] Phase P: langgraph-architect-expert invoque
- [ ] Phase C: python-developer-expert invoque
- [ ] Phase T: testing-expert invoque

Apres EPCT :
- [ ] Contexte partage mis a jour
- [ ] Resultat valide (tous tests passent)
- [ ] Resume fourni a l'utilisateur

---

*Version 2.0.0 - Janvier 2026*
*Workflow EPCT avec delegation aux sub-agents*
