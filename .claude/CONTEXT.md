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
Layer 1 — Capture : daily/YYYY-MM-DD_notes.md  (écriture libre, sans friction)
         ↓ pre-commit (spelling + TBC resolution, léger)
         ↓ enrich.py (Claude API, manuel, fin de journée)
Layer 2 — Digest  : modules/<catégorie>/<slug>/<module>_fiche.md (enrichi + dispatché)
                    modules/<catégorie>/<slug>/conversation.md (input manuel, copy-paste)
         ↓ quiz.py
Layer 3 — Master  : quiz multi-modules · errors-and-lessons/log.md
```

## File Structure — Current
```
data-engineering-notes/
  .claude/              # context files
  _templates/           # fiche-template.md, quiz-template.md
  modules/
    <catégorie>/<slug>/
      notes.md          # notes brutes existantes (legacy)
      fiche.md          # fiches existantes (legacy, à migrer)
      conversation.md   # extraits de conversations Claude.ai
  errors-and-lessons/
    log.md
  reviews/
    spaced-repetition.md
  scripts/
    enrich.py           # stub existant (à implémenter)
    improve_notes.py    # hook pre-commit existant
```

## File Structure — Target
*(supprimer cette section une fois atteinte)*
```
data-engineering-notes/
  .claude/              # context files
  _templates/           # fiche-template.md, quiz-template.md
  daily/
    YYYY-MM-DD_notes.md # capture quotidienne
  modules/
    <catégorie>/<slug>/
      <module>_fiche.md # fiche de révision (remplace fiche.md)
      conversation.md   # input manuel pour enrich.py
  errors-and-lessons/
    log.md
  scripts/
    enrich.py           # enrichissement + dispatch → <module>_fiche.md
    quiz.py             # quiz CLI multi-modules
  Makefile              # commandes dev
  pyproject.toml        # poetry + ruff + pytest config
```

## Environment
- **Dev**: local, macOS, pyenv + Poetry venv
- **Prod**: —
- **Credentials**: Claude API key (`.env`, jamais commité)
