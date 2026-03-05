# Design — Data Engineering Notes

> CONTAINS: problem space, use cases, user flows, solution approach, non-goals.
> NOT HERE: implementation details (→ CONTEXT.md), active tasks (→ TODOS.md), tech decisions (→ DECISIONS.md).
> Update when scope changes or a use case is validated/invalidated.
> Load tier: warm — update to cold when project reaches Running/Maintenance

---

## Problem Space
**Pain point**: pendant un bootcamp intensif, les notes brutes s'accumulent sans être consolidées ni révisées efficacement.
**Current state**: notes prises à la main, pas structurées, pas révisées — oubli garanti.
**Desired state**: capture sans friction → enrichissement automatique → révision ciblée sur les points faibles.


## Scope
**In scope**:
- Capture quotidienne libre (`daily/`)
- Enrichissement + dispatch automatisé via Claude API (`enrich.py`)
- Fiches de révision structurées par module (`<module>_fiche.md`)
- Quiz CLI avec log des erreurs

**Out of scope**:
- Spaced repetition (reporté)
- Partage / collaboration
- Interface web ou mobile
- Intégration avec des outils externes (Notion, Anki, etc.)
- Génération automatique au commit

## Learning by Doing — Cibles

**Outils cibles** (à intégrer progressivement dans ce projet) :
| Outil | Application dans ce projet |
|---|---|
| pyenv | gérer la version Python du projet |
| virtualenv / Poetry | isoler les dépendances |
| Ruff | lint + formatting (pre-commit) |
| pre-commit | hooks UC1 + UC4 |
| Click | CLI pour `enrich.py` et `quiz.py` |
| Loguru | logging dans les scripts |
| Pytest | tests unitaires des scripts |
| Sphinx | documentation des scripts |
| Makefile | commandes dev : `make enrich`, `make quiz`, `make test` |

**Notions cibles** (concepts bootcamp à appliquer à ce projet) :
| Notion | Application dans ce projet |
|---|---|
| Clean code | refactorer les scripts selon les conventions apprises |
| Testing / CI-CD | ajouter pytest + GitHub Actions |
| Docker | containeriser l'environnement si pertinent |
| Documentation | Sphinx sur les scripts, docstrings |
| Data pipelines | modéliser `enrich.py` comme un mini-pipeline |

## File Naming
- Notes quotidiennes : `YYYY-MM-DD_notes.md` dans `daily/`
- Fiches par module : `<module>_fiche.md` dans `modules/<catégorie>/<slug>/`

## Success Criteria
- [ ] Chaque jour de bootcamp a un `YYYY-MM-DD_notes.md`
- [ ] `enrich.py` met à jour les fiches des modules correspondants
- [ ] Chaque module a une `<module>_fiche.md` à jour avant les évaluations
- [ ] Les erreurs quiz sont loggées dans `errors-and-lessons/log.md`

## Use Cases

### UC1 — Capture quotidienne + pre-commit léger
**Actor**: Camille, pendant/après les cours
**Flow**: ouvre `daily/YYYY-MM-DD_notes.md`, écrit librement (notes brutes, questions, exemples, TBCs) → `git commit` déclenche le pre-commit
**Pre-commit scope** (sur lignes modifiées uniquement, très léger) :
- Spelling correction
- Remplacement des termes génériques (`trucs`, `choses`, `bidules`, `machin`, etc.) par des termes précis et contextuels
- Résolution des marqueurs incomplets : `TBC`, `TBD`, `?`, `??`, questions posées dans les notes
- Formatting : ajout de titres, restructuration si nécessaire — sans modifier, supprimer ou compléter le contenu existant
- Si l'intention est ambiguë et que Claude ne peut pas corriger/compléter avec certitude : ajouter le marqueur `TOCHECK` — ne jamais effacer ni ignorer le contenu original
- Ne jamais réécrire ou enrichir ce qui est déjà rédigé
**Expected output**: daily notes commité, orthographe corrigée, termes précisés, TBCs résolus, structure améliorée — sans enrichissement substantiel

### UC2 — Enrichissement en fin de journée
**Actor**: Camille, fin de journée
**Flow**: Camille copy-paste sa conversation Claude.ai dans `conversation.md` du module → `python scripts/enrich.py daily/YYYY-MM-DD_notes.md` → Claude lit daily notes + conversation.md → met à jour directement les `<module>_fiche.md` des modules concernés → résumé affiché → Camille review → commit
**Enrichissement scope** (plus complet que UC1, mais resté core) :
- Combler les lacunes conceptuelles, ajouter contexte, exemples concis
- Pas de blocs de code volumineux
- Dispatch direct vers les fiches des modules — pas de tagging intermédiaire
**Expected output**: une ou plusieurs `<module>_fiche.md` mises à jour



### UC3 — Quiz multi-modules
**Actor**: Camille, en révision
**Flow**: `python scripts/quiz.py <slug1> <slug2> ...` → questions générées depuis les `<module>_fiche.md` des modules sélectionnés + historique des erreurs → questions ratées re-posées
**Expected output**: score, erreurs loggées dans `errors-and-lessons/log.md`

### UC4 — Suggestions d'outils à appliquer (post-commit automatique)
**Actor**: système, déclenché à l'ajout d'une nouvelle fiche `<module>_fiche.md`
**Flow**: post-commit hook détecte un nouveau fichier `*_fiche.md` → croise le nom du module avec les outils et notions cibles → affiche des suggestions concrètes et non-bloquantes
**Expected output**: message informatif, ex: `"Nouvelle fiche 'testing-ci-cd' détectée → tu pourrais appliquer : pytest (tests pour enrich.py), GitHub Actions (CI)"`
**Implémentation**: post-commit hook (jamais bloquant) ou `make suggest`
**Suite**: si une suggestion est validée par Camille, elle est ajoutée aux tableaux outils/notions cibles dans DESIGN.md

### UC5 — Suggestion de nouveaux modules
**Actor**: Claude, proactivement ou à la demande
**Flow**: Claude analyse les sujets couverts en bootcamp et les modules existants → identifie des lacunes ou des concepts transversaux non encore capturés → propose des nouveaux slugs à ajouter à `modules/`
**Expected output**: liste de modules suggérés avec justification (ex: `"design-patterns manque — applicable à enrich.py et quiz.py"`)
**Note**: challenger la structure en place est un comportement attendu — les modules sont planifiés mais pas figés

## Solution Approach
Trois layers indépendants et composables : capture (Layer 1) → digest (Layer 2) → master (Layer 3). Chaque layer peut fonctionner sans le suivant. L'enrichissement Claude est le seul point de coût — déclenché manuellement pour rester intentionnel. Voir CONTEXT.md pour l'architecture technique.
