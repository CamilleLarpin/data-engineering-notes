# Context — Data Engineering Notes

> CONTAINS: current state, architecture overview, file structure, key dependencies.
> NOT HERE: decisions with rationale (→ DECISIONS.md), todos (→ TODOS.md), solution design (→ DESIGN.md).
> Update this file when architecture changes or a milestone completes.
> Load tier: warm

---

## Current State
**As of**: 2026-03-06
Bootcamp en cours (Feb 23 – Mar 27, 2026). Structure 3-layer opérationnelle. `enrich.py` opérationnel. `quiz.py` (Telegram bot) implémenté et testé manuellement — sélection de module + Q&A loop fonctionnel. Tests dans `src/tests/`. Dockerfile opérationnel — image buildée et testée localement (`make docker-build` + `make docker-run`). Prochain: GCP Compute Engine deploy.

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
  src/
    scripts/
      enrich.py         # enrichissement + dispatch → fiches (opérationnel)
      improve_notes.py  # hook pre-commit UC1 (opérationnel)
      quiz.py           # bot Telegram UC3 (opérationnel)
    tests/
      test_enrich.py
      test_improve_notes.py
      test_quiz.py
  Dockerfile            # opérationnel — local Docker testé
  app.yaml              # TODO (remplacé par Compute Engine)
  .envrc                # direnv — charge .env (commité, sans valeurs)
  Makefile
  pyproject.toml
```

## Environment
- **Dev**: local, macOS, pyenv + Poetry venv, direnv + `.envrc` → `.env`
- **CI**: GitHub Actions — pytest sur chaque push, secrets via GitHub Secrets
- **Prod**: Google App Engine Flexible — `app.yaml` référence les vars (jamais en dur)
- **Credentials**: Claude API key + secrets prod (`.env` local, GitHub Secrets en CI, GCP en prod — jamais commités)
