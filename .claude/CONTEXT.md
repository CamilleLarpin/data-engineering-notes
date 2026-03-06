# Context — Data Engineering Notes

> CONTAINS: current state, architecture overview, file structure, key dependencies.
> NOT HERE: decisions with rationale (→ DECISIONS.md), todos (→ TODOS.md), solution design (→ DESIGN.md).
> Update this file when architecture changes or a milestone completes.
> Load tier: warm

---

## Current State
**As of**: 2026-03-06
Bootcamp en cours (Feb 23 – Mar 27, 2026). Structure 3-layer opérationnelle. `enrich.py` implémenté et testé — enrichissement des fiches depuis `daily/` fonctionnel. `quiz.py` (Telegram bot) pas encore implémenté. Layer 1 (capture) active — `daily/` utilisé depuis 2026-02-24.

## Architecture

3-layer learning system :

```
Layer 1 — Capture : daily/YYYY-MM-DD/notes.md              (écriture libre, sans friction)
                    daily/YYYY-MM-DD/conversation_YYYY-MM-DD[_N].md (optionnel, zéro ou plusieurs)
         ↓ pre-commit (spelling + TBC resolution, léger)
         ↓ enrich.py (Claude API, manuel, fin de journée)
Layer 2 — Digest  : modules/<catégorie>/<slug>/<module>_fiche.md (enrichi + dispatché)
         ↓ quiz.py
Layer 3 — Master  : quiz multi-modules · errors-and-lessons/log.md
```

## File Structure — Current
```
data-engineering-notes/
  .claude/              # context files
  daily/
    YYYY-MM-DD/
      notes_YYYY-MM-DD.md
      conversation_YYYY-MM-DD[_N].md
  modules/
    <catégorie>/<slug>/
      <slug>_fiche.md
  errors-and-lessons/
    log.md
  reviews/
    spaced-repetition.md
  src/scripts/
    enrich.py           # enrichissement + dispatch → fiches (opérationnel)
    improve_notes.py    # hook pre-commit UC1 (opérationnel)
  tests/
    test_enrich.py
  .envrc                # direnv — charge .env (commité, sans valeurs)
  Makefile
  pyproject.toml
```

## File Structure — Target
*(supprimer cette section une fois atteinte)*
```
data-engineering-notes/
  .claude/              # context files
  daily/
    YYYY-MM-DD/
      notes_YYYY-MM-DD.md
      conversation_YYYY-MM-DD[_N].md
  modules/
    <catégorie>/<slug>/
      <slug>_fiche.md
  errors-and-lessons/
    log.md
  src/scripts/
    enrich.py
    quiz.py             # bot Telegram (python-telegram-bot)
  tests/
    test_enrich.py
    test_quiz.py
  Dockerfile            # image Python pour GAE Flexible
  app.yaml              # config Google App Engine Flexible
  .envrc
  Makefile
  pyproject.toml
```

## Environment
- **Dev**: local, macOS, pyenv + Poetry venv, direnv + `.envrc` → `.env`
- **CI**: GitHub Actions — pytest sur chaque push, secrets via GitHub Secrets
- **Prod**: Google App Engine Flexible — `app.yaml` référence les vars (jamais en dur)
- **Credentials**: Claude API key + secrets prod (`.env` local, GitHub Secrets en CI, GCP en prod — jamais commités)
