# Workflow DEBUG : Root Cause Analysis & Fix

Ce workflow doit être suivi lors de la réception d'un rapport de bug ou d'une erreur inattendue.

---

## 1. Reproduire le Bug

- Isoler l'erreur via un script de test minimal ou un notebook.
- Identifier les entrées (payload) qui provoquent l'erreur.
- Examiner les logs détaillés (et les traces LangSmith si disponibles).

## 2. Analyser (Root Cause Analysis)

- Remonter la pile d'exécution (stack trace).
- Vérifier les états du graphe (`State`) juste avant l'erreur.
- Vérifier les intégrations externes (API, DB) : sont-elles disponibles ? Les secrets sont-ils corrects ?

## 3. Planifier le Fix

- Proposer une correction qui traite la cause racine, pas seulement le symptôme.
- Vérifier les effets de bord potentiels.

## 4. Appliquer & Vérifier

- Appliquer le correctif via `replace` ou `write_file`.
- Lancer le script de reproduction pour confirmer la correction.
- Lancer la suite de tests complète avec `uv run pytest` pour s'assurer de l'absence de régression.

## 5. Documenter (Prévenir)

- Si le bug est complexe, ajouter un commentaire "Pourquoi" dans le code.
- Si nécessaire, mettre à jour `@skills/` pour ajouter une "Bonne Pratique" évitant ce type de bug à l'avenir.
