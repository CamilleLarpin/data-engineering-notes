# Conversations — git-and-github

<!-- Entrées ajoutées par Claude Code à partir des liens partagés -->

## Session du 24 février 2026
<!-- source: (pasted) -->

**[Question/Sujet]** Créer un repo GitHub depuis le terminal avec `gh` CLI

**[Explication]**
Deux approches possibles :

**`git init`** → quand on part d'un dossier existant sans repo GitHub.

**`gh repo create`** → quand on part de zéro, c'est plus propre : crée le repo sur GitHub ET clone en local en une commande.

```bash
gh repo create data-engineering-notes --public --clone
cd data-engineering-notes
```

Si `gh` n'est pas authentifié sur l'ordi local :
```bash
gh auth login
# Choisir : GitHub.com → SSH → Login with a web browser
```

Pourquoi créer le repo sur son **ordi local** plutôt que sur la VM du bootcamp ? Les notes pédagogiques sont de la documentation personnelle, pas du code lié à l'infra. Elles doivent **survivre à la VM** (supprimée en fin de bootcamp). Règle : code du bootcamp → VM ; notes et révision → local.

**[Insight clé]** `gh repo create --public --clone` = créer + cloner en une commande. Toujours distinguer ce qui vit sur la VM (code d'exercice) de ce qui vit en local (notes, docs personnelles).

---
