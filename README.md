# Data Engineering Bootcamp — Notes & Révisions (Feb 23 – Mar 27, 2026)

> Notes personnelles, fiches de révision et quiz du bootcamp Data Engineering.

---

## Workflow

```
Notes brutes (cours)  →  Fiche Claude (synthèse)  →  Quiz Telegram  →  Révision espacée
     notes.md         →       fiche.md             →    quiz.py      →  spaced-repetition.md
```

---

## Commandes

```bash
make enrich dir=daily/YYYY-MM-DD/   # Génère les fiches via Claude API
make quiz                            # Lance le bot Telegram quiz
make tests                           # Exécute les tests (pytest)
make lint                            # Vérifie le code (ruff check)
make format                          # Formate le code (ruff format)
make docker-build                    # Construit l'image Docker
make docker-run                      # Lance le bot en container
```

**Exemples :**

```bash
# Enrichir les notes du 10 mars
make enrich dir=daily/2026-03-10/

# Lancer le bot en local
make quiz

# Lancer le bot en container (prod)
make docker-build && make docker-run
```

---

## Usage courant

### Dispatcher une conversation Claude.ai

1. Dans Claude.ai, clique **Share** → copie le lien public
2. Dans Claude Code, écris : `dispatche : https://claude.ai/share/...`
3. Claude Code lit la conversation, trie par module, met à jour les `conversation.md` concernés

### Ajouter des notes

Ouvre `modules/<dossier>/notes.md` et prends des notes librement.

### Générer une fiche

```bash
make enrich dir=daily/YYYY-MM-DD/
```

Ou manuellement — coller dans Claude :

```
Voici mes notes sur [module] :
<contenu de notes.md>

Génère une fiche en suivant ce template :
<contenu de _templates/fiche-template.md>
```

### Générer un quiz

```
Voici ma fiche sur [module] :
<contenu de fiche.md>

Génère un quiz de 3 questions en suivant ce template :
<contenu de _templates/quiz-template.md>
```

### Logger une erreur

Ajoute une entrée dans `errors-and-lessons/log.md`.

---

## Index des modules

### Prep-Work

| Date | Module | Notes | Fiche | Quiz |
|------|--------|-------|-------|------|
| Feb | Setup | [notes](modules/2026-02-00_prep-work_setup/notes.md) | [fiche](modules/2026-02-00_prep-work_setup/fiche.md) | [quiz](modules/2026-02-00_prep-work_setup/quiz.md) |
| Feb | Data Types & Data Structures | [notes](modules/2026-02-00_prep-work_data-types-and-data-structures/notes.md) | [fiche](modules/2026-02-00_prep-work_data-types-and-data-structures/fiche.md) | [quiz](modules/2026-02-00_prep-work_data-types-and-data-structures/quiz.md) |
| Feb | Control Flow | [notes](modules/2026-02-00_prep-work_control-flow/notes.md) | [fiche](modules/2026-02-00_prep-work_control-flow/fiche.md) | [quiz](modules/2026-02-00_prep-work_control-flow/quiz.md) |
| Feb | Functions & Modules | [notes](modules/2026-02-00_prep-work_functions-and-modules/notes.md) | [fiche](modules/2026-02-00_prep-work_functions-and-modules/fiche.md) | [quiz](modules/2026-02-00_prep-work_functions-and-modules/quiz.md) |
| Feb | Object-Oriented Programming | [notes](modules/2026-02-00_prep-work_object-oriented-programming/notes.md) | [fiche](modules/2026-02-00_prep-work_object-oriented-programming/fiche.md) | [quiz](modules/2026-02-00_prep-work_object-oriented-programming/quiz.md) |

### Basics

| Date | Module | Notes | Fiche | Quiz |
|------|--------|-------|-------|------|
| Feb 23 | Terminal | [notes](modules/2026-02-23_basics_terminal/notes.md) | [fiche](modules/2026-02-23_basics_terminal/fiche.md) | [quiz](modules/2026-02-23_basics_terminal/quiz.md) |
| Feb 23 | Git & GitHub | [notes](modules/2026-02-23_basics_git-and-github/notes.md) | [fiche](modules/2026-02-23_basics_git-and-github/fiche.md) | [quiz](modules/2026-02-23_basics_git-and-github/quiz.md) |

### Data-Handling

| Date | Module | Notes | Fiche | Quiz |
|------|--------|-------|-------|------|
| Feb 24 | SQL Basics | [notes](modules/2026-02-24_data-handling_sql-basics/notes.md) | [fiche](modules/2026-02-24_data-handling_sql-basics/fiche.md) | [quiz](modules/2026-02-24_data-handling_sql-basics/quiz.md) |
| Feb 24 | SQL Beginner | [notes](modules/2026-02-24_data-handling_sql-beginner/notes.md) | [fiche](modules/2026-02-24_data-handling_sql-beginner/fiche.md) | [quiz](modules/2026-02-24_data-handling_sql-beginner/quiz.md) |
| Feb 25 | SQL Advanced | [notes](modules/2026-02-25_data-handling_sql-advanced/notes.md) | [fiche](modules/2026-02-25_data-handling_sql-advanced/fiche.md) | [quiz](modules/2026-02-25_data-handling_sql-advanced/quiz.md) |
| Feb 25 | SQL CRUD | [notes](modules/2026-02-25_data-handling_sql-crud/notes.md) | [fiche](modules/2026-02-25_data-handling_sql-crud/fiche.md) | [quiz](modules/2026-02-25_data-handling_sql-crud/quiz.md) |
| Feb 26 | NumPy | [notes](modules/2026-02-26_data-handling_numpy/notes.md) | [fiche](modules/2026-02-26_data-handling_numpy/fiche.md) | [quiz](modules/2026-02-26_data-handling_numpy/quiz.md) |
| Feb 26 | Pandas | [notes](modules/2026-02-26_data-handling_pandas/notes.md) | [fiche](modules/2026-02-26_data-handling_pandas/fiche.md) | [quiz](modules/2026-02-26_data-handling_pandas/quiz.md) |

### AI-Engineering

| Date | Module | Notes | Fiche | Quiz |
|------|--------|-------|-------|------|
| Feb 27 | ML Introduction | [notes](modules/2026-02-27_ai-engineering_ml-introduction/notes.md) | [fiche](modules/2026-02-27_ai-engineering_ml-introduction/fiche.md) | [quiz](modules/2026-02-27_ai-engineering_ml-introduction/quiz.md) |
| Mar 02 | Attention & Transformers | [notes](modules/2026-03-02_ai-engineering_attention-transformers/notes.md) | [fiche](modules/2026-03-02_ai-engineering_attention-transformers/fiche.md) | [quiz](modules/2026-03-02_ai-engineering_attention-transformers/quiz.md) |
| Mar 03 | Agentic | [notes](modules/2026-03-03_ai-engineering_agentic/notes.md) | [fiche](modules/2026-03-03_ai-engineering_agentic/fiche.md) | [quiz](modules/2026-03-03_ai-engineering_agentic/quiz.md) |

### Software-Engineering

| Date | Module | Notes | Fiche | Quiz |
|------|--------|-------|-------|------|
| Mar 04 | Clean Code & Documentation | [notes](modules/2026-03-04_software-engineering_clean-code-documentation/notes.md) | [fiche](modules/2026-03-04_software-engineering_clean-code-documentation/fiche.md) | [quiz](modules/2026-03-04_software-engineering_clean-code-documentation/quiz.md) |
| Mar 05 | Testing & CI/CD | [notes](modules/2026-03-05_software-engineering_testing-ci-cd/notes.md) | [fiche](modules/2026-03-05_software-engineering_testing-ci-cd/fiche.md) | [quiz](modules/2026-03-05_software-engineering_testing-ci-cd/quiz.md) |
| Mar 06 | Docker | [notes](modules/2026-03-06_software-engineering_docker/notes.md) | [fiche](modules/2026-03-06_software-engineering_docker/fiche.md) | [quiz](modules/2026-03-06_software-engineering_docker/quiz.md) |
| Mar 19 | Docker Compose | [notes](modules/2026-03-19_software-engineering_docker-compose/notes.md) | [fiche](modules/2026-03-19_software-engineering_docker-compose/fiche.md) | [quiz](modules/2026-03-19_software-engineering_docker-compose/quiz.md) |

### MLOps

| Date | Module | Notes | Fiche | Quiz |
|------|--------|-------|-------|------|
| Mar 09 | Productionizing ML Code | [notes](modules/2026-03-09_mlops_productionizing-ml-code/notes.md) | [fiche](modules/2026-03-09_mlops_productionizing-ml-code/fiche.md) | [quiz](modules/2026-03-09_mlops_productionizing-ml-code/quiz.md) |
| Mar 10 | Experiment Tracking & Model Registry | [notes](modules/2026-03-10_mlops_experiment-tracking-model-registry/notes.md) | [fiche](modules/2026-03-10_mlops_experiment-tracking-model-registry/fiche.md) | [quiz](modules/2026-03-10_mlops_experiment-tracking-model-registry/quiz.md) |
| Mar 11 | ML Pipelines | [notes](modules/2026-03-11_mlops_ml-pipelines/notes.md) | [fiche](modules/2026-03-11_mlops_ml-pipelines/fiche.md) | [quiz](modules/2026-03-11_mlops_ml-pipelines/quiz.md) |
| Mar 12 | Model Serving | [notes](modules/2026-03-12_mlops_model-serving/notes.md) | [fiche](modules/2026-03-12_mlops_model-serving/fiche.md) | [quiz](modules/2026-03-12_mlops_model-serving/quiz.md) |
| Mar 13 | Flask | [notes](modules/2026-03-13_mlops_flask/notes.md) | [fiche](modules/2026-03-13_mlops_flask/fiche.md) | [quiz](modules/2026-03-13_mlops_flask/quiz.md) |

### Data-Pipelines

| Date | Module | Notes | Fiche | Quiz |
|------|--------|-------|-------|------|
| Mar 16 | dbt Fundamentals | [notes](modules/2026-03-16_data-pipelines_dbt-fundamentals/notes.md) | [fiche](modules/2026-03-16_data-pipelines_dbt-fundamentals/fiche.md) | [quiz](modules/2026-03-16_data-pipelines_dbt-fundamentals/quiz.md) |
| Mar 17 | dbt Advanced | [notes](modules/2026-03-17_data-pipelines_dbt-advanced/notes.md) | [fiche](modules/2026-03-17_data-pipelines_dbt-advanced/fiche.md) | [quiz](modules/2026-03-17_data-pipelines_dbt-advanced/quiz.md) |
| Mar 20 | Spark | [notes](modules/2026-03-20_data-pipelines_spark/notes.md) | [fiche](modules/2026-03-20_data-pipelines_spark/fiche.md) | [quiz](modules/2026-03-20_data-pipelines_spark/quiz.md) |
| Mar 24 | Airflow | [notes](modules/2026-03-24_data-pipelines_airflow/notes.md) | [fiche](modules/2026-03-24_data-pipelines_airflow/fiche.md) | [quiz](modules/2026-03-24_data-pipelines_airflow/quiz.md) |
| Mar 25 | Airflow Advanced | [notes](modules/2026-03-25_data-pipelines_airflow-advanced/notes.md) | [fiche](modules/2026-03-25_data-pipelines_airflow-advanced/fiche.md) | [quiz](modules/2026-03-25_data-pipelines_airflow-advanced/quiz.md) |

### Cloud-Architecture

| Date | Module | Notes | Fiche | Quiz |
|------|--------|-------|-------|------|
| Mar 18 | GCP Fundamentals | [notes](modules/2026-03-18_cloud-architecture_gcp-fundamentals/notes.md) | [fiche](modules/2026-03-18_cloud-architecture_gcp-fundamentals/fiche.md) | [quiz](modules/2026-03-18_cloud-architecture_gcp-fundamentals/quiz.md) |
| Mar 23 | Spark ML | [notes](modules/2026-03-23_cloud-architecture_spark-ml/notes.md) | [fiche](modules/2026-03-23_cloud-architecture_spark-ml/fiche.md) | [quiz](modules/2026-03-23_cloud-architecture_spark-ml/quiz.md) |
| Mar 26 | Terraform | [notes](modules/2026-03-26_cloud-architecture_terraform/notes.md) | [fiche](modules/2026-03-26_cloud-architecture_terraform/fiche.md) | [quiz](modules/2026-03-26_cloud-architecture_terraform/quiz.md) |
| Mar 27 | Kubernetes | [notes](modules/2026-03-27_cloud-architecture_kubernetes/notes.md) | [fiche](modules/2026-03-27_cloud-architecture_kubernetes/fiche.md) | [quiz](modules/2026-03-27_cloud-architecture_kubernetes/quiz.md) |

---

## Structure du repo

```
.
├── modules/                              # Un dossier par module
│   └── YYYY-MM-DD_catégorie_module/
│       ├── notes.md                      # Notes brutes de cours
│       ├── fiche.md                      # Fiche de révision synthétisée
│       └── quiz.md                       # Quiz de révision
├── daily/                                # Capture quotidienne libre
│   └── YYYY-MM-DD/
│       ├── notes_YYYY-MM-DD.md
│       └── conversation_YYYY-MM-DD.md
├── src/scripts/
│   ├── enrich.py                         # Claude → fiche.md (lancement manuel)
│   └── quiz.py                           # Bot Telegram quiz multi-modules
├── _templates/
│   ├── fiche-template.md
│   └── quiz-template.md
├── errors-and-lessons/
│   └── log.md
├── Dockerfile
├── app.yaml                              # Config Google App Engine
└── Makefile
```

## Stack technique

| Composant | Choix |
|-----------|-------|
| Enrichissement | Claude API (Sonnet) |
| Quiz | Bot Telegram (`python-telegram-bot`) |
| Containerisation | Docker |
| Déploiement | Google App Engine Flexible |
| CI/CD | GitHub Actions (pytest → build → deploy) |
| Env vars | direnv local · GitHub Secrets CI · app.yaml prod |
| Lint / Format | Ruff |
| Tests | pytest |
