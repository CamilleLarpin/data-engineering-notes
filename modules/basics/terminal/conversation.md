# Conversations — terminal

<!-- Entrées ajoutées par Claude Code à partir des liens partagés -->

## Session du 24 février 2026
<!-- source: (pasted) -->

**[Question/Sujet]** Alias shell et `~/.zshrc` — créer des raccourcis de navigation

**[Explication]**
Un **alias** est un raccourci — un nom de commande custom qui mappe vers une commande plus longue.

```bash
alias myproject="cd ~/code/CamilleLarpin/student-challenges-de/curriculum/00-Basics/04-SQL/data"
alias ll="ls -la"
alias ..="cd .."
alias gst="git status"
```

Quand tu tapes `myproject`, le shell remplace silencieusement par la commande complète.

**`~/.zshrc`** : fichier de config que Zsh lit à chaque ouverture de terminal. C'est là qu'on stocke tout ce qu'on veut disponible dans chaque session — alias, variables d'environnement, path settings. Penser à : "instructions que Zsh lit avant de te passer la main."

**`source ~/.zshrc`** : normalement, les modifications à `~/.zshrc` ne prennent effet qu'à l'ouverture d'un nouveau terminal. `source` force Zsh à re-lire et appliquer le fichier immédiatement, sans redémarrer.

```bash
# Workflow :
# 1. Éditer ~/.zshrc → sauvegarder
# 2. Appliquer sans redémarrer :
source ~/.zshrc
# 3. Utiliser l'alias immédiatement
```

Si tu ajoutes un alias à `~/.zshrc` mais ne lances pas `source ~/.zshrc`, il sera disponible à la prochaine ouverture de terminal.

**[Insight clé]** Mettre un alias de navigation dans `~/.zshrc` pour chaque projet/module du bootcamp — ça économise beaucoup de frappe au quotidien. Mettre à jour les alias au fur et à mesure qu'on progresse dans le curriculum.

---
