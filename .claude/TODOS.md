# Todos — Data Engineering Notes

> CONTAINS: active milestones, next actions, blocked items for this project.
> NOT HERE: decisions (→ DECISIONS.md), completed work (archive or delete when done), cross-project tasks.
> This is a working scratchpad for Camille + Claude. Keep it current — stale todos are noise.
> Load tier: warm

---

## Now — Séquence cible

### 1. quiz.py → Bot Telegram — UC3 ✓ done
- [x] Implémenter `quiz.py` comme bot Telegram (`python-telegram-bot`)
- [x] `/quiz` liste les modules non-vides (inline keyboard), démarre une session
- [x] Le bot envoie une question, attend la réponse, donne le feedback
- [x] Erreurs loggées dans `errors-and-lessons/log.md`
- [x] Tests pytest pour la logique quiz (hors Telegram)
- [x] Entrée Makefile : `make quiz`
- [x] Tests déplacés dans `src/tests/`

### 2. Docker ✓ done
- [x] Créer `Dockerfile` (image Python pour le bot Telegram)
- [x] Tester localement : `docker build` + `docker run`

### 3. GCP — Compute Engine VM
- [ ] Créer Artifact Registry repo (gcloud CLI ou Console)
- [ ] Build image `--platform linux/amd64` pour GCP
- [ ] Push image vers Artifact Registry
- [ ] Créer VM Compute Engine, installer Docker
- [ ] Pull image + lancer le conteneur sur la VM
- [ ] Makefile : `build_gcp`, `push_gcp`, `deploy_gcp`

### 4. CI/CD complet : test → build → deploy
- [ ] Mettre à jour `.github/workflows/` : ajouter build Docker + deploy GAE
- [ ] Tester la pipeline complète end-to-end

## TBC — Phase 4 — UC4/UC5
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
- [x] `LOG_LEVEL` env var — debug silencieux par défaut, visible avec `LOG_LEVEL=DEBUG`
- [x] `fail_fast: true` + `verbose: true` retiré — pre-commit s'arrête au premier échec, sortie propre
- [x] Phase 2 complète : hook testé sur modification, suppression, tests pytest ajoutés
- [x] GitHub Actions CI — pytest sur chaque push (`.github/workflows/pytest-ci.yml`)
- [x] direnv configuré — `.envrc` → `dotenv .env`, `.env` dans `.gitignore`
- [x] `enrich.py` implémenté et opérationnel — enrichissement fiches depuis `daily/` (UC2)
- [x] Bug model ID Anthropic corrigé (`claude-sonnet-4-20250514` → `claude-sonnet-4-6`)
- [x] `quiz.py` implémenté — bot Telegram, sélection module + Q&A loop + log erreurs (UC3)
- [x] Tests déplacés dans `src/tests/` — structure unifiée
