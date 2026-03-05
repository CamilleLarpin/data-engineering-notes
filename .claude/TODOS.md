# Todos — Data Engineering Notes

> CONTAINS: active milestones, next actions, blocked items for this project.
> NOT HERE: decisions (→ DECISIONS.md), completed work (archive or delete when done), cross-project tasks.
> This is a working scratchpad for Camille + Claude. Keep it current — stale todos are noise.
> Load tier: warm

---

## Now — Phase 1 : Réorganisation des dossiers
- [ ] Renommer `fiche.md` → `<module>_fiche.md` dans tous les modules existants
- [ ] Créer le dossier `daily/`
- [ ] Migrer/archiver les `notes.md` existants (legacy) si nécessaire
- [ ] Vérifier que la file structure courante correspond à la target (CONTEXT.md)

## Next — Phase 2 : Capture (Layer 1)
- [ ] Configurer pre-commit UC1 : spelling + résolution TBC/TBD/? sur `daily/*_notes.md`
- [ ] Tester le hook sur un premier fichier de capture

## Next — Phase 3 : Enrich (Layer 2)
- [ ] Implémenter `enrich.py` : lit daily notes + conversation.md → met à jour `<module>_fiche.md`
- [ ] CLI avec Click
- [ ] Logging avec Loguru
- [ ] Tests avec Pytest
- [ ] Entrée Makefile : `make enrich`

## TBC — Phase 4
- [ ] À définir après Phase 3 (quiz CLI, post-commit UC4, ou autre)

## Blocked
— aucun

## Done (recent — clear periodically)
- [x] Architecture 3-layer définie (Capture → Digest → Master)
- [x] Structure `.claude/` initialisée avec tous les fichiers templates
- [x] DESIGN.md complet : UCs, scope, outils/notions cibles
