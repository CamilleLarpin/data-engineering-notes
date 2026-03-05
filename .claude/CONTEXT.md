# Context — Data Engineering Notes

> CONTAINS: current state, architecture overview, file structure, key dependencies.
> NOT HERE: decisions with rationale (→ DECISIONS.md), todos (→ TODOS.md), solution design (→ DESIGN.md).
> Update this file when architecture changes or a milestone completes.
> Load tier: warm

---

## Current State
**As of**: 2026-03-05
Bootcamp en cours (Feb 23 – Mar 27, 2026). Structure de base des modules existante, pre-commit configuré avec Ruff. `enrich.py` et `quiz.py` pas encore implémentés. Layer 1 (capture) non encore utilisée — `daily/` n'existe pas encore.

## Architecture

3-layer learning system :

```
Layer 1 — Capture    : daily/YYYY-MM-DD.md  (écriture libre, sans friction)
         ↓ enrich.py (Claude API, manuel)
Layer 2 — Structure  : modules/<catégorie>/<slug>/conversation.md (enrichi + dispatché)
         ↓ generate / quiz.py
Layer 3 — Mastery    : fiche✅.md · errors-and-lessons/log.md · reviews/spaced-repetition.md
```

## File Structure
```
data-engineering-notes/
  .claude/              # context files
  _templates/           # fiche-template.md, quiz-template.md
  daily/                # YYYY-MM-DD.md — capture brute (à créer)
  modules/
    <catégorie>/<slug>/
      notes.md          # dispatché + enrichi par Claude
      fiche✅.md        # fiche de révision structurée
      conversation.md   # extraits dispatché depuis daily/
  errors-and-lessons/
    log.md              # erreurs quiz, points faibles
  reviews/
    spaced-repetition.md
  scripts/
    enrich.py           # enrichissement + dispatch (à implémenter)
    quiz.py             # quiz CLI (à implémenter)
```

## Key Dependencies
| Dependency | Version/URL | Purpose |
|---|---|---|
| Python | 3.x | scripts enrich.py + quiz.py |
| Claude API | Sonnet | enrichissement + dispatch |
| pre-commit | — | Ruff lint + typos au commit |
| Ruff | — | lint + formatting |

## Environment
- **Dev**: local, macOS
- **Prod**: —
- **Credentials**: Claude API key (à définir dans .env ou env var)
