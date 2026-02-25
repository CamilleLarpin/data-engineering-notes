# Instructions pour Claude Code — Data Engineering Bootcamp

## Contexte

Ce repo centralise les notes, fiches de révision et quiz d'un bootcamp Data Engineering (Feb 23 – Mar 27, 2026). Chaque module a un dossier dans `modules/` avec 4 fichiers : `notes.md`, `fiche.md`, `quiz.md`, `conversation.md`.

## Commande : dispatche

**Déclencheur :** l'utilisateur écrit `dispatche : <url>` (lien de conversation Claude.ai partagée publiquement).

**Ce que tu dois faire :**

1. Fetch le contenu de l'URL avec WebFetch
2. Lire la conversation en entier
3. Identifier tous les modules abordés (faire correspondre avec les dossiers dans `modules/`)
4. Pour chaque module identifié, **appender** le contenu pertinent dans `modules/<dossier>/conversation.md`

**Format d'une entrée dans `conversation.md` :**

```markdown
## Session du JJ mois AAAA
<!-- source: <url> -->

**[Question/Sujet]** Résumé de la question ou du sujet abordé

**[Explication]** Explication de Claude, verbatim si elle est claire et concise, résumée sinon. Garder les analogies, exemples concrets, reformulations simples. Garder les blocs de code tels quels.

**[Insight clé]** Ce qui était une zone de flou et qui a été clarifié.

---
```

**Règles de tri :**
- Un échange peut apparaître dans plusieurs `conversation.md` si plusieurs modules sont abordés
- Garder le niveau de détail des explications de Claude (ne pas trop résumer)
- Trimmer : salutations, reformulations meta ("peux-tu expliquer autrement"), confirmations courtes
- Toujours appender (jamais écraser) — ajouter après le dernier contenu existant
- Après dispatch, afficher un résumé : quels modules ont été mis à jour et combien d'échanges ajoutés

## Structure du repo

```
modules/<YYYY-MM-DD>_<catégorie>_<slug>/
  notes.md          # notes brutes de cours (écrites par l'utilisateur)
  fiche.md          # fiche de révision synthétisée
  quiz.md           # quiz de révision
  conversation.md   # extraits de conversations Claude.ai, triés par module
_templates/
  fiche-template.md
  quiz-template.md
errors-and-lessons/log.md
reviews/spaced-repetition.md
generate.sh         # CLI : ./generate.sh <fiche|quiz> <slug>
```

## Script generate.sh

`./generate.sh fiche <slug>` — génère un prompt prêt à copier pour créer `fiche.md` à partir de `notes.md` + `conversation.md`
`./generate.sh quiz <slug>` — idem pour `quiz.md`, en partant de `fiche.md` si elle existe
