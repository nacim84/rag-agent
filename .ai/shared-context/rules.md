# 📋 Protocole de Gestion du Contexte Partagé

## 🎯 Objectif

Ce protocole définit comment **tous les agents** (Main-Agent et Sub-Agents) doivent gérer le contexte partagé pour :
- Économiser les tokens du main-agent
- Exploiter la fenêtre de contexte de chaque sub-agent
- Assurer la continuité du contexte entre les agents
- Tracer tout ce qui a été fait pendant la session

---

## 🔵 Règles pour TOUS les Agents (Main-Agent + Sub-Agents)

### ✅ Au DÉBUT de chaque tâche

**OBLIGATION 1 : LIRE LE CONTEXTE**

1. **TOUJOURS LIRE** `ai/shared-context/session-active.md` AVANT de commencer
2. Identifier dans le fichier :
   - 🎯 Objectif global de la session
   - 📝 Ce qui a déjà été fait par les autres agents
   - 🏗️ Décisions architecturales prises
   - 🚧 Problèmes rencontrés et solutions appliquées
   - 🔄 Notes de handoff du dernier agent
3. **Annoncer à l'utilisateur** :
   ```
   📖 Contexte chargé : [résumé en 1-2 phrases de ce qui a été fait]
   ```

**Exemple** :
```
📖 Contexte chargé : Le projet utilise Next.js 14 avec Server Actions.
L'explorator-project-agent a identifié une architecture fullstack native.
Le saas-architect-validator-agent a validé le système de multi-tenancy.
```

---

### 🔄 PENDANT la tâche

1. Travailler de manière autonome dans sa fenêtre de contexte
2. Prendre des notes mentales des **décisions importantes** prises
3. Noter les **fichiers modifiés** et **actions réalisées**
4. Identifier les **problèmes rencontrés** et **solutions appliquées**

---

### 💾 À la FIN de chaque tâche

**OBLIGATION 2 : METTRE À JOUR LE CONTEXTE**

1. **TOUJOURS METTRE À JOUR** `ai/shared-context/session-active.md`
2. Ajouter une nouvelle section dans `## 📝 Travail Effectué` avec le format suivant :

```markdown
### [NOM_AGENT] - [YYYY-MM-DD HH:MM]
**Tâche** : [Description courte de la tâche effectuée]

**Actions réalisées** :
- ✅ [Action 1]
- ✅ [Action 2]
- ✅ [Action 3]

**Fichiers modifiés** :
- `path/to/file1.ts` - [Description de la modification]
- `path/to/file2.tsx` - [Description de la modification]

**Décisions prises** :
- 🎯 [Décision 1] : [Justification]
- 🎯 [Décision 2] : [Justification]

**Problèmes rencontrés et solutions** :
- 🚧 [Problème] : [Solution appliquée]

**Prochaines étapes suggérées** :
- [ ] [Étape 1]
- [ ] [Étape 2]

---
```

3. Mettre à jour **État Actuel** si nécessaire (Phase, Progression)
4. Mettre à jour **Contexte Technique Important** si de nouvelles découvertes
5. Mettre à jour **Handoff Notes** avec des notes pour le prochain agent
6. **Annoncer à l'utilisateur** :
   ```
   💾 Contexte mis à jour avec [résumé des actions en 1 phrase]
   ```

**Exemple** :
```
💾 Contexte mis à jour : Exploration complète de l'architecture effectuée,
stack Next.js 14 identifiée, 23 fichiers analysés.
```

---

## 🎯 Format de Résumé (Template à Copier)

Voici le template exact à utiliser lors de la mise à jour du contexte :

```markdown
### [NOM_AGENT] - [YYYY-MM-DD HH:MM]
**Tâche** : [Description courte]

**Actions réalisées** :
- ✅ [Action 1]
- ✅ [Action 2]

**Fichiers modifiés** :
- `file.ts` - [Modification]

**Décisions prises** :
- 🎯 [Décision] : [Justification]

**Problèmes rencontrés et solutions** :
- 🚧 [Problème] : [Solution]

**Prochaines étapes suggérées** :
- [ ] [Étape suivante]

---
```

---

## 🔄 Archivage des Sessions

### Quand archiver ?

Archiver la session active quand :
- L'utilisateur démarre une **nouvelle session de travail**
- Une **feature complète** a été terminée et validée
- L'utilisateur demande explicitement de **clore la session**

### Comment archiver ?

1. Lire `ai/shared-context/session-active.md`
2. Identifier le **numéro de session** suivant (vérifier `ai/shared-context/session-history/`)
3. Copier `session-active.md` vers `ai/shared-context/session-history/session-XXX.md`
4. Réinitialiser `session-active.md` avec le template vide
5. Annoncer :
   ```
   🗄️ Session archivée : session-XXX.md
   📄 Nouvelle session active créée
   ```

---

## 📊 Statistiques et Métriques

Chaque session archivée doit contenir en fin de fichier :

```markdown
## 📊 Métriques de la Session

- **Durée totale** : [X heures]
- **Agents impliqués** : [Liste des agents]
- **Fichiers modifiés** : [Nombre total]
- **Problèmes résolus** : [Nombre]
- **Décisions architecturales** : [Nombre]
- **État final** : ✅ TERMINÉ / ⚠️ EN COURS / ❌ ABANDONNÉ
```

---

## ⚠️ Cas Particuliers

### Si le fichier `session-active.md` est vide ou corrompu

1. Initialiser avec le template de base
2. Demander à l'utilisateur l'objectif de la session
3. Documenter le problème dans `## 🚧 Problèmes Rencontrés`

### Si le contexte devient trop volumineux (>10 000 lignes)

1. Archiver la session actuelle
2. Créer une nouvelle session avec un **résumé** de l'ancienne
3. Référencer l'ancienne session dans `## 📚 Ressources et Références`

### Si plusieurs agents travaillent en parallèle

1. Chaque agent ajoute sa section **sans supprimer** les sections des autres
2. Respecter l'ordre chronologique (timestamp)
3. Si conflit de modification, le **dernier agent** résout le conflit

---

## 🚀 Exemples Concrets

### Exemple 1 : explorator-project-agent

```markdown
### explorator-project-agent - 2025-12-18 14:30
**Tâche** : Exploration exhaustive de l'architecture du projet

**Actions réalisées** :
- ✅ Analyse de l'arborescence complète (145 fichiers)
- ✅ Identification de la stack : Next.js 14, TypeScript, Tailwind
- ✅ Détection des patterns : Server Actions, App Router
- ✅ Analyse des dépendances : 42 packages npm

**Fichiers clés identifiés** :
- `app/layout.tsx` - Layout principal avec providers
- `lib/actions/*.ts` - Server Actions pour l'API
- `components/ui/*` - Composants Shadcn/UI

**Décisions prises** :
- 🎯 Architecture fullstack Next.js native (pas de backend séparé)
- 🎯 Utilisation de Server Actions pour toutes les mutations

**Prochaines étapes suggérées** :
- [ ] Valider l'architecture avec saas-architect-validator-agent
- [ ] Planifier l'implémentation de la nouvelle feature

---
```

### Exemple 2 : saas-architect-validator-agent

```markdown
### saas-architect-validator-agent - 2025-12-18 14:45
**Tâche** : Validation de l'architecture pour feature "Partage de workspace"

**Actions réalisées** :
- ✅ Audit des 5 Piliers SaaS
- ✅ Vérification de l'isolation des données (tenant_id présent)
- ✅ Validation du modèle RBAC existant
- ✅ Analyse de la performance (Prisma avec indexes optimisés)

**Décisions prises** :
- 🎯 VERT : Architecture validée pour multi-tenancy
- 🎯 Recommandation : Ajouter rate limiting sur les invitations
- 🎯 Recommandation : Implémenter audit log pour partage

**Problèmes rencontrés et solutions** :
- 🚧 Manque de validation Zod sur les rôles : Solution = Créer schema RoleEnum

**Prochaines étapes suggérées** :
- [ ] Implémenter le schema Zod pour les rôles
- [ ] Ajouter rate limiting avec Upstash Redis
- [ ] fullstack-expert-agent peut commencer l'implémentation

---
```

---

## 🏁 Checklist de Conformité

Avant de terminer votre tâche, vérifiez :

- [ ] ✅ J'ai LU le contexte partagé au début de ma tâche
- [ ] ✅ J'ai ANNONCÉ à l'utilisateur le contexte chargé
- [ ] ✅ J'ai DOCUMENTÉ toutes mes actions dans `session-active.md`
- [ ] ✅ J'ai utilisé le FORMAT correct (timestamp, actions, fichiers, décisions)
- [ ] ✅ J'ai AJOUTÉ des notes de handoff pour le prochain agent
- [ ] ✅ J'ai ANNONCÉ à l'utilisateur la mise à jour du contexte

---

**Version** : 1.0.0
**Dernière mise à jour** : 2026-01-10
**Auteur** : Nacim84
