# Data Engineering Notes — Claude Context

> Load tier: hot

@~/.claude/CLAUDE.md

## Project
**Purpose**: Centraliser notes + fiches de révision du bootcamp Data Engineering (Feb 23 – Mar 27, 2026)
**Status**: 🔵 Building
**Repo**: —
**Stack**: Python · Claude API · pre-commit · Ruff

## Context Files
- .claude/CONTEXT.md — current state, architecture, file structure, dependencies
- .claude/DECISIONS.md — active decisions only (resolved → DECISIONS_ARCHIVE.md)
- .claude/LESSONS.md — what to avoid: mistakes, patterns, gotchas (never delete)
- .claude/DESIGN.md — problem space, use cases, scope, outils/notions cibles
- .claude/TODOS.md — active milestones, next actions, blocked items

## Active Constraints
- Toujours appender, jamais écraser (`conversation_YYYY-MM-DD.md`, `errors-and-lessons/log.md`)
- `conversation_YYYY-MM-DD.md` : langue de la conversation source
- `<module>_fiche.md` : toujours en anglais
- `errors-and-lessons/log.md` : toujours en anglais
- `enrich.py` lancé manuellement — jamais au commit

## Learning by Doing
Quand un nouveau module est ajouté ou qu'un sujet est couvert, suggérer proactivement quels outils ou notions cibles (voir DESIGN.md) pourraient être mis en application dans ce projet.

## Quick Reference
- Scripts: `python scripts/enrich.py daily/YYYY-MM-DD/` · `python scripts/quiz.py <slug>`
- Daily: `daily/YYYY-MM-DD/` (`notes_YYYY-MM-DD.md` · `conversation_YYYY-MM-DD[_N].md`)
- Modules: `modules/<catégorie>/<slug>/` (`fiche_<module>.md` uniquement)

## Current Focus
Phase 1 (réorganisation dossiers) → voir .claude/TODOS.md
