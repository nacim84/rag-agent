# Product Requirements Document (PRD) - RAG Agent Ingestion Pipeline

**Projet :** rag-agent
**Date :** 16 Janvier 2026
**Version :** 1.0
**Statut :** Draft

---

## 1. Vue d'ensemble

### 1.1 Objectif
Ce document décrit les spécifications pour la migration et l'implémentation du pipeline d'ingestion de documents (initialement conçu sous n8n "Add_Documents_Workflow") vers l'architecture Python `rag-agent`.
L'objectif est de créer un système robuste, idempotent et automatisé pour ingérer, traiter et vectoriser des documents provenant de Google Drive afin d'alimenter la base de connaissances (RAG) de l'agent IA.

### 1.2 Périmètre
Le système doit surveiller trois sources de données distinctes (dossiers Google Drive), gérer différents types de fichiers (structurés et non structurés), et alimenter une base de données PostgreSQL vectorielle.

---

## 2. Architecture des Données

### 2.1 Sources de Données (Google Drive)
Le système doit surveiller et distinguer les fichiers provenant de trois dossiers spécifiques :

| Nom Logique | Dossier Source (Google Drive) | Table Vectorielle Cible |
|-------------|-------------------------------|-------------------------|
| **Comptable** | `RAG_COMPTABLE` | `documents_comptable` |
| **Exploitation** | `RAG_EXPLOITATION` | `documents_exploitation` |
| **Transaction** | `RAG_TRANSACTION` | `documents_transaction` |

### 2.2 Schéma Base de Données (PostgreSQL)

Le système repose sur un schéma relationnel et vectoriel mixte.

#### Tables Métadonnées & Relationnelles
1.  **`document_metadata`**
    *   Stocke les infos générales des fichiers ingérés.
    *   Colonnes : `id` (PK, File ID), `title`, `url`, `created_at`, `schema` (pour fichiers structurés).

2.  **`transaction_rows`**
    *   Stocke les données brutes extraites des fichiers structurés (CSV/Excel).
    *   Colonnes : `id` (Serial), `transaction_row_id` (FK -> document_metadata.id), `transaction_row_content` (JSONB).

3.  **`rag_chat_memory`**
    *   Mémoire conversationnelle (déjà prévue dans le boilerplate).

4.  **`transaction_qonto`**
    *   Table spécifique pour les données bancaires structurées (Qonto).

#### Tables Vectorielles (pgvector)
Chaque domaine possède sa propre table vectorielle pour une isolation sémantique :
*   `documents_comptable`
*   `documents_exploitation`
*   `documents_transaction`

---

## 3. Spécifications Fonctionnelles

### 3.1 Déclencheurs (Triggers)
*   **Polling :** Vérification périodique (ex: toutes les minutes via Celery Beat) des dossiers Google Drive.
*   **Événements gérés :** `fileCreated`, `fileUpdated`.
*   **Idempotence :** Avant tout traitement, le système doit nettoyer les anciennes entrées associées à l'`id` du fichier (suppression des lignes dans `document_metadata`, `transaction_rows` et les tables vectorielles).

### 3.2 Pipeline de Traitement

#### Étape 1 : Identification & Nettoyage
*   Récupérer les métadonnées du fichier (ID, Nom, MIME Type, Lien).
*   Identifier la source (`comptable`, `exploitation`, `transaction`).
*   Exécuter les requêtes de nettoyage (DELETE) pour éviter les doublons.

#### Étape 2 : Routage par Type de Fichier
Le traitement diffère selon le type MIME :

**A. Fichiers Structurés (Excel, CSV)**
*   **MIME Types :** `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, `text/csv`.
*   **Action :**
    1.  Extraire les données ligne par ligne.
    2.  Détecter le schéma (clés des colonnes).
    3.  Insérer les métadonnées avec le schéma détecté dans `document_metadata`.
    4.  Insérer chaque ligne sous forme d'objet JSON dans `transaction_rows`.
    5.  Convertir les données en texte pour vectorisation (concaténation).

**B. Fichiers Non-Structurés (PDF, GDoc)**
*   **MIME Types :** `application/pdf`, `application/vnd.google-apps.document`.
*   **Action :**
    1.  Télécharger le contenu.
    2.  Utiliser un outil de parsing avancé (équivalent au sous-workflow `Docling_Chunker_Tool`).
    3.  Découper le texte (Chunking).

#### Étape 3 : Vectorisation (Embeddings)
*   **Modèle :** Google Gemini Embeddings (via `langchain-google-genai`).
*   **Chunking Strategy :** `RecursiveCharacterTextSplitter` (Chunk Size: 2000, Overlap: recommandé ~200).
*   **Stockage :** Insertion des vecteurs et métadonnées dans la table cible correspondante (`documents_*`).

---

## 4. Spécifications Techniques

### 4.1 Stack Technologique
*   **Langage :** Python 3.11 (via UV).
*   **Orchestration :** LangGraph (pour le flux de traitement) & Celery (pour le scheduling/polling).
*   **Base de données :** PostgreSQL 16 + extension `vector`.
*   **LLM Integration :** `langchain-google-genai`.
*   **Drive Integration :** `google-api-python-client`.

### 4.2 Variables d'Environnement Requises
(À ajouter au `.env` si manquant)
```env
GOOGLE_API_KEY=...             # Pour Gemini Embeddings
GOOGLE_CREDENTIALS_PATH=...    # Pour accès Drive (Service Account ou OAuth)
POSTGRES_DB=langgraph_db
POSTGRES_USER=langgraph_user
POSTGRES_PASSWORD=...
```

---

## 5. Plan d'Implémentation

1.  **Database Migration :** Créer les scripts SQL (`scripts/init_db.sql` ou Alembic) pour reproduire les tables identifiées.
2.  **Google Drive Service :** Implémenter `src/tools/google/drive.py` pour le polling et le téléchargement.
3.  **Parsers :** Implémenter les parsers CSV/Excel (avec `pandas` ou `csv`) et PDF (avec `pypdf` ou `docling`).
4.  **Embeddings Service :** Configurer le provider Gemini dans LangChain.
5.  **Ingestion Workflow :** Créer un graphe LangGraph (`src/agents/workflows/ingestion_graph.py`) reproduisant la logique du switch et du traitement.
6.  **Scheduler :** Configurer une tâche Celery Beat pour lancer le workflow d'ingestion périodiquement.

---

## 6. Critères de Succès
*   Les fichiers déposés dans les dossiers Drive apparaissent dans les tables vectorielles correspondantes.
*   La modification d'un fichier Drive met à jour ses embeddings sans créer de doublons.
*   Les fichiers Excel/CSV alimentent correctement la table `transaction_rows`.
*   Le système gère les erreurs (fichiers corrompus, API quota) sans crasher le worker.
