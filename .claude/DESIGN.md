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
- Fiches de révision structurées par module (`fiche✅.md`)
- Quiz CLI avec log des erreurs
- Spaced repetition basé sur l'historique des erreurs

**Out of scope**:
- Partage / collaboration
- Interface web ou mobile
- Intégration avec des outils externes (Notion, Anki, etc.)
- Génération automatique au commit

## Success Criteria
- [ ] Chaque jour de bootcamp a un `daily/YYYY-MM-DD.md`
- [ ] `enrich.py` dispatche correctement vers les modules correspondants
- [ ] Chaque module a une `fiche✅.md` à jour avant les évaluations
- [ ] Les erreurs quiz sont loggées et remontées en spaced repetition

## Use Cases

### UC1 — Capture quotidienne
**Actor**: Camille, pendant/après les cours
**Flow**: ouvre `daily/YYYY-MM-DD.md`, écrit librement (notes brutes, questions, exemples)
**Expected output**: fichier sauvegardé, commité — sans structure imposée

### UC2 — Enrichissement en fin de journée
**Actor**: Camille, fin de journée
**Flow**: `python scripts/enrich.py daily/YYYY-MM-DD.md` → Claude enrichit + dispatche → résumé affiché → Camille review → commit
**Expected output**: sections enrichies appendées dans les `conversation.md` des modules correspondants

### UC3 — Génération de fiche
**Actor**: Camille, avant révision ou évaluation
**Flow**: `generate fiche <slug>` → Claude lit notes.md + conversation.md + template → écrit `fiche✅.md`
**Expected output**: fiche structurée prête à réviser

### UC4 — Quiz sur un topic
**Actor**: Camille, en révision
**Flow**: `python scripts/quiz.py <slug>` → questions générées depuis `fiche✅.md` → erreurs loggées → questions ratées re-posées
**Expected output**: score, erreurs loggées dans `errors-and-lessons/log.md`

### UC5 — Spaced repetition
**Actor**: Camille, chaque matin
**Flow**: système remonte les points faibles à J+1, J+7, J+21 depuis `reviews/spaced-repetition.md`
**Expected output**: liste des topics à réviser aujourd'hui

## Solution Approach
Trois layers indépendants et composables : capture (Layer 1) → structure (Layer 2) → mastery (Layer 3). Chaque layer peut fonctionner sans le suivant. L'enrichissement Claude est le seul point de coût — déclenché manuellement pour rester intentionnel. Voir CONTEXT.md pour l'architecture technique.
