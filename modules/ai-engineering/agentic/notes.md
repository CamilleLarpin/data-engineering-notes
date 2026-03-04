# Notes — Agentic Systems

---

## Composants Clés (communs à tous les frameworks)

| Composant | Rôle |
|---|---|
| **LLM** | Le moteur de raisonnement — choisit les actions, planifie les étapes suivantes |
| **Outils / Fonctions** | Moyens d'agir : appeler des APIs, exécuter du code, chercher sur le web, interroger des BDs, utiliser un interpréteur de code, etc. |
| **Mémoire** | Contexte à court et long terme (voir section dédiée) |
| **Planification & Contrôle** | Structures comme les boucles ReAct (raisonner-agir), planificateurs, vérificateurs, évaluateurs, routeurs |
| **Orchestration** | Comment les étapes sont séquencées et supervisées ; mono vs multi-agent ; tentatives ; approbations humaines |
| **Sécurité & Garde-fous** | Contraintes, validation, HITL (Human-In-The-Loop), audits, logging/observabilité |

---

## La Boucle de l'Agent (modèle mental)

Une boucle simple que la plupart des frameworks implémentent :

```
1. Percevoir  → lire la tâche + contexte
2. Planifier  → décider de la meilleure action suivante (possiblement un appel d'outil)
3. Agir       → appeler cet outil (avec des arguments)
4. Réfléchir  → lire le résultat de l'outil, vérifier le succès, mettre à jour la mémoire
5. Répéter ou Terminer → continuer jusqu'à atteindre l'objectif, puis produire la réponse finale
```

Il s'agit du **pattern ReAct** (Reasoning + Acting) — la colonne vertébrale de la plupart des frameworks agentiques.

---

## Mémoire : Court terme vs Long terme

| Type | Ce que c'est | Comment ça fonctionne |
|---|---|---|
| **Court terme** | La conversation / fenêtre de contexte actuelle | Maintenu dans le contexte actif du LLM (prompt + historique) |
| **Long terme** | Connaissances persistantes entre les sessions | Stocké externement — récupéré via **RAG** (base vectorielle, recherche) |

**→ Question : "Est-ce que Claude fait déjà ça ?"**

Partiellement. Claude (claude.ai) a une mémoire conversationnelle **dans la session** (court terme), et une mémoire persistante optionnelle entre sessions (le système de "memories" qu'on voit dans les prompts système). Mais ce n'est **pas du RAG** — c'est de la synthèse manuelle stockée en texte. Du vrai RAG agentique, tu le construis toi-même : tu choisis la base vectorielle, le modèle d'embedding, la stratégie de récupération. Claude ne te cache pas cette complexité — il l'externalise.

---

## Types de Workflows : Automatisé vs IA vs Agentique

| Type | Définition | Exemple |
|---|---|---|
| **Workflow Automatisé** | Basé sur des règles, pas d'IA — déterministe | Tâche cron, déclencheur Zapier simple |
| **Workflow IA** | Étapes fixes + LLM sur certains nœuds — semi-déterministe | "Extraire → résumer avec GPT → envoyer email" |
| **Workflow Agentique** | L'agent décide lui-même les étapes — probabiliste | L'agent choisit ses outils, s'auto-corrige, itère |

**Règle de choix :** plus le workflow est critique/répétable → déterministe. Plus la tâche est ouverte/complexe → agentique.

---

## Workflows Multi-Agents

Quand une tâche est trop complexe pour un seul agent, on la découpe en agents spécialisés.

**Pourquoi ?**
- La **fenêtre de contexte** d'un LLM est limitée — un agent maître qui fait tout se noie
- La **spécialisation** améliore la qualité (un agent = une responsabilité claire)
- La **parallélisation** est possible (agents travaillant en parallèle)

**Patterns courants :**
- **Superviseur / Orchestrateur** → distribue les tâches aux sous-agents
- **Pipeline** → chaque agent passe son output au suivant
- **Débat / Révision** → un agent produit, un autre critique

---

## Bonnes Pratiques de Prompting pour les Systèmes Agentiques

- Spécifier l'**output attendu** (format, longueur, structure)
- Lister les **outils disponibles** et **quand les utiliser** (le LLM ne devine pas)
- Donner un **objectif clair** et des **critères d'arrêt** (sinon l'agent tourne en boucle)
- Préférer des **instructions positives** ("fais X") aux négatives ("ne fais pas Y")
- Inclure des **exemples** si le comportement attendu est non-trivial (few-shot)

---

## LangGraph / LangChain — Concepts Clés

| Concept | Définition |
|---|---|
| **State** | Mémoire partagée entre toutes les étapes du flux (dict mutable) |
| **Nodes** | Les étapes du graphe — chaque nœud est une fonction Python |
| **Edges** | Les liens entre nœuds — peuvent être conditionnels (routage) |
| **Graph** | L'ensemble nœuds + arêtes + état = le workflow complet |

**LangChain** = séquences linéaires (chaînes). **LangGraph** = graphes avec cycles, branches, retours en arrière.

---

## Variables d'Environnement

Les variables d'environnement permettent de **séparer la configuration du code** — clés API, URLs, secrets.

```bash
# Fichier .env (jamais commité)
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...
```

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

**Gestion par environnement :**
- **Local** : fichier `.env` chargé via `python-dotenv` ou `direnv` (`.envrc`)
- **Global** : variables système (`export VAR=value` dans `.bashrc`/`.zshrc`)
- **CI/CD / Cloud** : injectées par la plateforme (GitHub Secrets, GCP Secret Manager)
- Toujours ajouter `.env` au `.gitignore`

**Lien avec pyenv** : pyenv gère les *versions Python*, pas les variables d'environnement. Ce sont deux choses distinctes.

---

## Python : `*args` et `**kwargs`

```python
def ma_fonction(*args, **kwargs):
    print(args)   # tuple des arguments positionnels
    print(kwargs) # dict des arguments nommés

ma_fonction(1, 2, 3, nom="Alice", age=30)
# args   → (1, 2, 3)
# kwargs → {'nom': 'Alice', 'age': 30}
```

| Syntaxe | Nom | Ce que ça capture |
|---|---|---|
| `*args` | args | Arguments positionnels en surplus → **tuple** |
| `**kwargs` | kwargs | Arguments nommés en surplus → **dict** |

**Usage typique en agentique :** les SDKs comme LangChain passent souvent `**kwargs` pour transmettre des paramètres optionnels aux outils sans casser les signatures.

---

## Modèles Open Source vs Hébergé vs Propriétaire

| Tier | Exemples | Avantages | Inconvénients |
|---|---|---|---|
| **Local (open source)** | Ollama + Qwen, Llama, Mistral | Gratuit, privé, offline | Limité en performance, non scalable |
| **Hébergé open source** | Groq, Together AI, Hugging Face Inference | Rapide, quasi-gratuit, scalable | Dépendance réseau, données envoyées |
| **Propriétaire** | OpenAI, Anthropic, Google | Meilleure performance, support | Coût, données tierces |

**Ollama en local :** idéal pour développer/tester sans coût. En production, migrer vers un hébergeur.

```python
# Avec Ollama, appel compatible OpenAI SDK
llm = ChatOllama(model="qwen2.5:0.5b", tools=[...])
```

---

## Écosystème des Frameworks Agentiques (évolue rapidement)

Il n'y a pas de standard stable — choisir en fonction du besoin :

| Framework | Usage principal |
|---|---|
| **LangChain / LangGraph** | Agents Python, très répandu, bonne intégration d'outils |
| **CrewAI** | Multi-agent orienté "équipes" |
| **AutoGen** (Microsoft) | Multi-agent conversationnel |
| **Prefect / Airflow** | Orchestration de pipelines data (pas spécifiquement agentique) |
| **N8N** | No-code / low-code, prototypage rapide |

> Les frameworks évoluent quotidiennement — apprendre les **concepts** (boucle d'agent, outils, mémoire, état), pas la syntaxe d'un framework spécifique.