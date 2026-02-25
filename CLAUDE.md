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

**Langue :**
- `conversation.md` : rester fidèle à la langue de la conversation source (français si la conversation était en français, anglais si en anglais)
- `fiche.md` et `quiz.md` : toujours en anglais

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
```

## Commande : generate

**Déclencheur :** l'utilisateur écrit `generate fiche <slug>` ou `generate quiz <slug>` dans Claude Code.

**Ce que tu dois faire :**

1. Trouver le dossier du module correspondant au slug dans `modules/`
2. Lire `notes.md` et `conversation.md` du module (sources pour la fiche), ou `fiche.md` (source pour le quiz)
3. Lire le template correspondant dans `_templates/`
4. Générer le contenu en suivant le template
5. Écrire le résultat directement dans `fiche.md` ou `quiz.md` du module
6. Afficher un résumé : module trouvé, fichier écrit, nombre de sections générées

**Règles :**
- `fiche` : source = `notes.md` + `conversation.md`
- `quiz` : source = `fiche.md` si elle existe, sinon `notes.md` + `conversation.md`
- `fiche.md` et `quiz.md` sont toujours en **anglais**
- Si le fichier cible existe déjà, l'écraser (régénération complète)
- Une fois le fichier écrit, renommer le fichier avec ✅ dans le nom : `fiche.md` → `fiche✅.md`, `quiz.md` → `quiz✅.md`
