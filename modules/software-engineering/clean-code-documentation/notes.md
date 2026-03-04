# Notes — Clean Code & Documentation

## Gestion des environnements

### Outils principaux (du plus classique au plus moderne)

- **venv** — façon native Python de créer un environnement virtuel. Intégré à Python 3, pas besoin d'installer quoi que ce soit.
- **virtualenv** — alternative tierce à venv, plus de fonctionnalités, légèrement plus rapide.
- **pyenv** — gère plusieurs versions de Python sur la même machine (ex : 3.9, 3.11, 3.12 en parallèle). Ne gère pas les packages.
- **pyenv-virtualenv** — plugin de pyenv qui combine gestion de version Python + environnements virtuels.
- **conda** — gère à la fois les versions Python ET les packages. Très utilisé en data science, mais lourd.
- **uv** — outil moderne (Rust), remplaçant ultra-rapide de pip + venv. Tend à devenir le standard en production.

> **Principe clé** : Si on vise la mise en production, on configure l'environnement dès le début pour figer les dépendances et garantir la reproductibilité.

> **Attention** : Ne pas utiliser plusieurs gestionnaires d'environnements à la fois : redondance et risque de conflit.

### Commandes pyenv essentielles

```bash
pyenv versions                          # liste toutes les versions Python installées
pyenv virtualenvs                       # liste tous les environnements virtuels créés
pyenv virtualenv [version] nom_env      # crée un environnement (version optionnelle)
pyenv activate nom_env                  # active manuellement un environnement
pyenv local nom_env                     # lie un environnement à un dossier → crée .python-version
pyenv global nom_env                    # définit l'environnement par défaut (global)
```

**Environnement global** : environnement utilisé par défaut si aucun local n'est défini.

**Gestion locale recommandée** : utiliser `pyenv local` dans chaque projet. Pyenv lit automatiquement le fichier `.python-version` à la racine du dossier et active le bon environnement — pas besoin d'activer manuellement.

### pyenv local vs pyenv activate

- `pyenv activate` = activation manuelle. Si tu fermes ton terminal, c'est perdu. Tu dois le refaire à chaque session.
- `pyenv local` = écrit un fichier `.python-version` dans ton dossier. Pyenv le lit automatiquement à chaque fois que tu entres dans ce dossier — même après redémarrage. C'est la méthode recommandée en projet.

## Vérification et gestion des packages

```bash
pip list                              # liste tous les packages installés (format lisible)
pip freeze                            # idem, mais format requirements.txt (nom==version)
pip freeze > requirements.txt         # exporte les dépendances → fichier à committer
pip install -r requirements.txt       # recrée l'environnement à l'identique ailleurs
pip list | grep nom                   # filtre un package spécifique
```

### Différence pip list vs pip freeze

- **pip list** → lisible, pour inspecter
- **pip freeze** → machine-readable, pour reproduire l'environnement

### Pourquoi committer requirements.txt mais pas le dossier venv ?

Le dossier `venv` contient des binaires compilés pour ta machine (chemins absolus, OS spécifique). Il ne fonctionnerait pas sur la machine d'un collègue ou sur un serveur Linux.

`requirements.txt` est juste une liste d'instructions — n'importe quelle machine peut recréer l'environnement à partir de ça avec `pip install -r requirements.txt`. C'est la recette, pas le gâteau.

C'est d'ailleurs pourquoi on ajoute `venv/` ou `.venv/` dans le `.gitignore`.

## Structure d'un projet Python

```
src/                # tout le code Python
tests/              # tests unitaires (miroir de src/)
README.md
pyproject.toml      # configuration du projet (remplace setup.py)
requirements.txt    # dépendances figées
```

**pyproject.toml** — fichier de configuration standard (syntaxe TOML, similaire à YAML).
Définit le nom du package, la version, les dépendances, les outils (black, pytest...).

## Modules, Packages, Librairies

| Terme | Définition |
|---|---|
| Module | Un seul fichier `.py` |
| Package | Un dossier de modules avec un `__init__.py` |
| Librairie | Un package publié et installable via pip |

## Exécution de code Python

- **Script direct** : `python mon_script.py`
- **Import local** : `from src.utils import ma_fonction` — importe depuis un fichier local
- **Import module** : `import pandas` — importe depuis un package installé

`__name__ == "__main__"` s'exécute uniquement quand le fichier est lancé directement. Si importé, le bloc est ignoré.

## CLI en Python avec Click

**Click** — librairie pour créer des interfaces en ligne de commande en Python.

```python
import click

@click.command()
@click.argument('name')
def hello(name):
    print(f"Hello {name}")

if __name__ == "__main__":
    hello()
```

## Outils de qualité de code

### Linter

Un linter analyse ton code sans l'exécuter et signale :
- Les erreurs de syntaxe
- Le non-respect des conventions (PEP8 en Python)
- Les variables inutilisées, imports manquants, etc.

**Le linter détecte, mais ne modifie pas le code.**

**Ruff** — linter Python recommandé. Codé en Rust, 10-100x plus rapide que ses équivalents.
Reprend les règles de Pylint + Flake8 en un seul outil.

### Formatter

Un formatter **modifie automatiquement** le code pour le rendre conforme aux conventions.

**Black** — formatter Python standard. Pas de configuration, opinionated.
**Ruff** — peut aussi formatter (remplace Black progressivement).

| | Linter | Formatter |
|---|---|---|
| Détecte les problèmes | ✅ | ✅ |
| Corrige automatiquement | ❌ | ✅ |
| Exemple | Ruff, Pylint | Black, Ruff |

> Les linters et formatters existent dans tous les langages (ESLint pour JS, RuboCop pour Ruby...).
> Ruff est spécifique Python.

## Pre-commit hooks

Les hooks pre-commit s'exécutent automatiquement avant chaque commit et ne traitent que les fichiers modifiés.

**2 types de pre-commit** :
- Ceux qui modifient automatiquement le code (formatters)
- Ceux qui renvoient une erreur et bloquent le commit (linters)

Dès qu'on fait un commit, le pre-commit s'exécute. On peut créer ses propres hooks personnalisés.

## Sécurité : Injection SQL

Attaque où un utilisateur malveillant insère du SQL dans une entrée pour manipuler la base de données.

```python
# ❌ Vulnérable
query = f"SELECT * FROM users WHERE name = '{user_input}'"
# Si user_input = "'; DROP TABLE users; --" → catastrophe

# ✅ Sécurisé — paramètres liés
query = "SELECT * FROM users WHERE name = ?"
cursor.execute(query, (user_input,))
```

**La règle** : **Ne jamais construire une requête SQL par concaténation de strings.**

## Typing en Python

Python supporte le typage optionnel depuis Python 3.5+ :

```python
def process_data(data: list[str]) -> dict[str, int]:
    return {item: len(item) for item in data}
```

Les annotations de type améliorent la lisibilité et permettent la détection d'erreurs avec des outils comme `mypy`.

## Logging

Il y a un module `logging` de base dans Python, mais il est recommandé de ne pas l'utiliser directement.

**Loguru** — standard moderne pour le logging en Python, plus simple et puissant.

```python
from loguru import logger

logger.info("Message d'information")
logger.error("Erreur survenue")
```

## Documentation

### Principe de base

**Règle** : Code lisible pour quelqu'un d'autre qui pourrait être moi dans 3 jours.

### Exemples de référence

- **✅ Belle documentation** : scikit-learn
- **❌ Documentation perfectible** : matplotlib

### Outils de génération

**Sphinx** — outil standard pour générer de la documentation automatiquement à partir du code Python et des docstrings.

Peut générer des sites web complets de documentation à partir des commentaires dans le code.