# Data Engineering Notes — Claude Context

> Load tier: hot

@~/.claude/CLAUDE.md

## Project
**Purpose**: Centraliser notes + fiches de révision du bootcamp Data Engineering (Feb 23 – Mar 27, 2026)
**Status**: 🔵 Building
**Repo**: —
**Stack**: Python · Claude API · pre-commit · Ruff

## Context Files
- .claude/CONTEXT.md — current state, architecture, file structure, key dependencies
- .claude/DECISIONS.md — active decisions only (resolved → DECISIONS_ARCHIVE.md)
- .claude/LESSONS.md — what to avoid: mistakes, patterns, gotchas (never delete)
- .claude/DESIGN.md — problem space, use cases, user flows, solution approach, non-goals
- .claude/TODOS.md — active milestones, next actions, blocked items

## Active Constraints
- Toujours appender, jamais écraser (`conversation.md`, `errors-and-lessons/log.md`)
- `conversation.md` : langue de la conversation source
- `fiche.md` : toujours en anglais
- `errors-and-lessons/log.md` : toujours en anglais
- `enrich.py` lancé manuellement — jamais au commit

## Quick Reference
- Scripts: `python scripts/enrich.py daily/YYYY-MM-DD.md` · `python scripts/quiz.py <slug>`
- Modules: `modules/<catégorie>/<slug>/` (notes.md · fiche✅.md · conversation.md)

## Current Focus
Phase 1 (pre-commit: Ruff + typos) et Phase 2 (enrich.py) sont les deux prochaines features à construire. Voir .claude/TODOS.md.

---

## Commande : enrich

**Déclencheur :** `python scripts/enrich.py daily/YYYY-MM-DD.md`

**Ce que Claude fait :**

1. Lit `daily/YYYY-MM-DD.md`
2. Enrichit le contenu (comble les lacunes, ajoute contexte, corrige spelling)
3. Tague chaque section avec le topic correspondant (matching slugs dans `modules/`)
4. Dispatche le contenu tagué vers `modules/<topic>/conversation.md` (toujours append)
5. Affiche un résumé : quels modules mis à jour, combien d'échanges ajoutés

**Règles :**
- Toujours appender, jamais écraser
- Garder le niveau de détail des notes originales
- Trimmer : salutations, meta-commentaires, confirmations courtes

---

## Commande : dispatche (legacy)

**Déclencheur :** `dispatche : <url>` (lien de conversation Claude.ai partagée publiquement)

**Ce que Claude fait :**

1. Fetch le contenu de l'URL avec WebFetch
2. Identifie tous les modules abordés
3. Appende le contenu pertinent dans `modules/<catégorie>/<slug>/conversation.md`
4. Si quiz + erreurs, appende dans `errors-and-lessons/log.md`
5. Affiche résumé : modules mis à jour, échanges ajoutés, erreurs loggées

**Format d'une entrée dans `conversation.md` :**

```markdown
## Session du JJ mois AAAA
<!-- source: <url> -->

**[Question/Sujet]** Résumé de la question ou du sujet abordé

**[Explication]** Explication de Claude, verbatim si claire et concise, résumée sinon. Garder analogies, exemples, blocs de code tels quels.

**[Insight clé]** Ce qui était flou et a été clarifié.

---
```

**Format d'une entrée dans `errors-and-lessons/log.md` :**

```markdown
| JJ/MM/AAAA | catégorie/slug | Description courte de l'erreur | Leçon / ce qu'il faut retenir |
```

---

## Commande : generate

**Déclencheur :** `generate fiche <slug>`

**Ce que Claude fait :**

1. Trouve le dossier du module dans `modules/`
2. Lit `notes.md` et `conversation.md`
3. Lit `_templates/fiche-template.md`
4. Génère la fiche en suivant le template
5. Écrit dans `fiche.md` puis renomme en `fiche✅.md`

**Règles :**
- Toujours en anglais
- Écraser si le fichier existe déjà (régénération complète)
