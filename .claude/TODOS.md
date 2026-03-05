# Todos — Data Engineering Notes

> CONTAINS: active milestones, next actions, blocked items for this project.
> NOT HERE: decisions (→ DECISIONS.md), completed work (archive or delete when done), cross-project tasks.
> This is a working scratchpad for Camille + Claude. Keep it current — stale todos are noise.
> Load tier: warm

---

## Now
- [ ] Phase 1 — Pre-commit: configurer Ruff + typos sur `daily/*.md` (lint + spelling, non-destructif, ne bloque jamais)

## Next
- [ ] Phase 2 — `enrich.py`: lit `daily/YYYY-MM-DD.md`, enrichit via Claude API, tague par topic, dispatche vers `modules/<topic>/conversation.md`
- [ ] Créer le dossier `daily/` et ajouter un premier fichier de capture

## Blocked
— aucun

## Done (recent — clear periodically)
- [x] Architecture 3-layer définie (daily → enrich → modules → quiz)
- [x] Roadmap phases 1–6 documentée
- [x] Structure `.claude/` initialisée
