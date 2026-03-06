# Decisions — Data Engineering Notes

> CONTAINS: active choices made during this project — what was chosen, alternatives considered, rationale.
> NOT HERE: implementation steps, todos, bug reports, lessons (→ LESSONS.md), resolved decisions (→ DECISIONS_ARCHIVE.md).
> Archive at 100 lines → DECISIONS_ARCHIVE.md.
> When a decision applies beyond this project: flag with `→ PROMOTE: DECISIONS_GLOBAL.md — [reason]`
> Load tier: cool

---

## Format
```
## [category] Decision title
- **Decision**: what was chosen
- **Rationale**: why — include alternatives considered and why they were rejected
- **Date**: YYYY-MM-DD
- **Status**: active | superseded by [title] | archived
```

---

## [architecture] Learning-first: fichiers comme outputs, pas point de départ
- **Decision**: les fichiers `modules/` sont des outputs générés — pas le point de départ du workflow. La capture se fait dans `daily/`, libre et sans friction.
- **Rationale**: forcer une structure dès la prise de notes crée de la friction et décourage la capture. Les LLMs peuvent structurer après coup bien mieux qu'un humain en temps réel.
- **Date**: 2026-03-05
- **Status**: active

## [architecture] `daily/` comme Layer 1 de capture
- **Decision**: un fichier par jour `daily/YYYY-MM-DD.md`, écriture libre, sans structure imposée.
- **Rationale**: minimise la friction à la capture. Alternative (écrire directement dans modules/) rejetée car impose une décision de catégorisation en temps réel.
- **Date**: 2026-03-05
- **Status**: active

## [tooling] `enrich.py` lancé manuellement, pas au commit
- **Decision**: `enrich.py` est déclenché manuellement en fin de journée — jamais automatiquement au commit.
- **Rationale**: l'enrichissement Claude coûte des tokens et prend du temps — doit rester intentionnel. Le pre-commit est réservé aux checks non-destructifs (lint, typos).
- **Date**: 2026-03-05
- **Status**: active

## [tooling] Pre-commit scope limité à lint + typos
- **Decision**: pre-commit exécute uniquement Ruff (lint/formatting) et typos (spelling). Ne bloque jamais le commit.
- **Rationale**: les checks au commit doivent être rapides et non-destructifs. Tout ce qui modifie le contenu (enrichissement, dispatch) est hors scope du pre-commit.
- **Date**: 2026-03-05
- **Status**: active

## [stack] FastAPI pour le quiz (UC3) — web app, pas CLI
- **Decision**: `quiz.py` devient une web app FastAPI déployée sur Google App Engine Flexible, pas une CLI locale.
- **Rationale**: déploiement sur GAE implique une interface HTTP. FastAPI est léger, rapide à mettre en place, et cohérent avec le contexte MLOps/Data Engineering du bootcamp. Alternative (CLI uniquement) rejetée car incompatible avec le déploiement cloud.
- **Date**: 2026-03-06
- **Status**: active

## [stack] Docker + Google App Engine Flexible pour le déploiement
- **Decision**: containerisation via Docker, déploiement sur Google App Engine Flexible (pas Standard).
- **Rationale**: GAE Flexible supporte des runtimes custom via Dockerfile — nécessaire pour contrôler précisément l'environnement Python. GAE Standard rejeté car trop contraint sur les runtimes.
- **Date**: 2026-03-06
- **Status**: active

## [tooling] direnv + .envrc pour le chargement local des env vars
- **Decision**: `direnv` avec `.envrc` charge automatiquement `.env` en local. `.envrc` est commité (sans valeurs), `.env` est ignoré par git.
- **Rationale**: évite les `source .env` manuels; cohérent avec le pattern par contexte (local / CI / prod). Alternative (Makefile `export`) rejetée car non automatique.
- **Date**: 2026-03-06
- **Status**: active

## [conventions] Gestion des env vars par contexte d'exécution
- **Decision**: Local → `.envrc` charge `.env`; CI → GitHub Secrets injectés comme env vars dans le workflow; Prod → `app.yaml` référence les vars (jamais de valeurs en dur dans aucun fichier commité).
- **Rationale**: chaque contexte a ses contraintes propres. Centraliser dans un seul mécanisme forcerait soit des secrets en clair (local), soit une complexité inutile (prod). La règle commune : aucune valeur sensible dans le dépôt.
- **Date**: 2026-03-06
- **Status**: active
