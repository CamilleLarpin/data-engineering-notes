# Instructions pour Claude Code — Data Engineering Bootcamp

## Contexte

Ce repo centralise les notes et fiches de révision d'un bootcamp Data Engineering (Feb 23 – Mar 27, 2026). Chaque module a un dossier dans `modules/` avec 3 fichiers : `notes.md`, `fiche.md`, `conversation.md`. Les quiz sont générés à la demande par Claude.ai (qui a accès au repo GitHub).

## Commande : dispatche

**Déclencheur :** l'utilisateur écrit `dispatche : <url>` (lien de conversation Claude.ai partagée publiquement).

**Ce que tu dois faire :**

1. Fetch le contenu de l'URL avec WebFetch
2. Lire la conversation en entier
3. Identifier tous les modules abordés (faire correspondre avec les dossiers dans `modules/`)
4. Pour chaque module identifié, **appender** le contenu pertinent dans `modules/<catégorie>/<slug>/conversation.md`
5. Si la conversation contient un quiz et des erreurs de l'utilisateur, **appender** dans `errors-and-lessons/log.md`

**Format d'une entrée dans `conversation.md` :**

```markdown
## Session du JJ mois AAAA
<!-- source: <url> -->

**[Question/Sujet]** Résumé de la question ou du sujet abordé

**[Explication]** Explication de Claude, verbatim si elle est claire et concise, résumée sinon. Garder les analogies, exemples concrets, reformulations simples. Garder les blocs de code tels quels.

**[Insight clé]** Ce qui était une zone de flou et qui a été clarifié.

---
```

**Format d'une entrée dans `errors-and-lessons/log.md` :**

Appender une ligne par erreur dans le tableau existant :

```markdown
| JJ/MM/AAAA | catégorie/slug | Description courte de l'erreur | Leçon / ce qu'il faut retenir |
```

**Règles de tri :**
- Un échange peut apparaître dans plusieurs `conversation.md` si plusieurs modules sont abordés
- Garder le niveau de détail des explications de Claude (ne pas trop résumer)
- Trimmer : salutations, reformulations meta ("peux-tu expliquer autrement"), confirmations courtes
- Toujours appender (jamais écraser) — ajouter après le dernier contenu existant
- Après dispatch, afficher un résumé : quels modules ont été mis à jour, combien d'échanges ajoutés, et combien d'erreurs loggées

**Langue :**
- `conversation.md` : rester fidèle à la langue de la conversation source (français si la conversation était en français, anglais si en anglais)
- `fiche.md` : toujours en anglais
- `errors-and-lessons/log.md` : toujours en anglais

## Structure du repo

```
modules/
  <catégorie>/              # ex: prep-work, basics, data-handling, ai-engineering...
    <slug>/                 # ex: sql-advanced, data-types-and-data-structures...
      notes.md              # notes brutes de cours (écrites par l'utilisateur)
      fiche✅.md            # fiche de révision (✅ dans le nom = générée)
      conversation.md       # extraits de conversations Claude.ai, triés par module
_templates/
  fiche-template.md
errors-and-lessons/log.md   # journal global des erreurs faites en quiz
reviews/spaced-repetition.md
```

## Commande : generate

**Déclencheur :** l'utilisateur écrit `generate fiche <slug>` dans Claude Code.

**Ce que tu dois faire :**

1. Trouver le dossier du module correspondant au slug dans `modules/`
2. Lire `notes.md` et `conversation.md` du module
3. Lire le template dans `_templates/fiche-template.md`
4. Générer le contenu en suivant le template
5. Écrire le résultat directement dans `fiche.md` du module
6. Renommer le fichier avec ✅ dans le nom : `fiche.md` → `fiche✅.md`
7. Afficher un résumé : module trouvé, fichier écrit

**Règles :**
- `fiche.md` est toujours en **anglais**
- Si le fichier cible existe déjà, l'écraser (régénération complète)
