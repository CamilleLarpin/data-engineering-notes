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
