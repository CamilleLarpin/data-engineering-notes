# Todos — Data Engineering Notes

> CONTAINS: active milestones, next actions, blocked items for this project.
> NOT HERE: decisions (→ DECISIONS.md), completed work (archive or delete when done), cross-project tasks.
> This is a working scratchpad for Camille + Claude. Keep it current — stale todos are noise.
> Load tier: warm

---

## Now — Phase 2 : Capture (Layer 1) — UC1
- [ ] Tester le hook sur modification au milieu d'un fichier
- [ ] Tester le hook sur suppression de lignes
- [ ] Ajouter tests pytest pour ces scénarios

## Next — Phase 3 : Enrich (Layer 2) — UC2
- [ ] Implémenter `enrich.py` : lit `notes_YYYY-MM-DD.md` + `conversation_*.md` → met à jour `fiche_<module>.md`
- [ ] CLI avec Click
- [ ] Logging avec Loguru
- [ ] Tests pytest pour `enrich.py`
- [ ] Entrée Makefile : `make enrich`

## TBC — Phase 4 — UC3/UC4/UC5
- [ ] Quiz CLI (`quiz.py`) — UC3
- [ ] Post-commit hook suggestions — UC4
- [ ] Suggestion nouveaux modules — UC5

## Blocked
— aucun

## Done (recent — clear periodically)
- [x] Architecture 3-layer définie (Capture → Digest → Master)
- [x] Structure `.claude/` initialisée avec tous les fichiers templates
- [x] DESIGN.md complet : UCs, scope, outils/notions cibles
- [x] Phase 1 : Réorganisation des dossiers — structure cible atteinte
- [x] `improve_notes.py` implémenté — pre-commit UC1
- [x] pytest configuré — 12 tests unitaires (`improve_notes.py`)
- [x] Makefile — `make tests`, `make lint`, `make format`
- [x] Ruff configuré — lint + format (E, F, I, N, line-length 100)
- [x] Pre-commit hook — ruff + improve-notes opérationnel
- [x] Loguru ajouté — debug sur toutes les fonctions
- [x] Bug `\ No newline at end of file` corrigé
- [x] `filter_new_lines` extraite et testée
