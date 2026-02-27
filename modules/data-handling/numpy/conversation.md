# Conversations — numpy

<!-- Entrées ajoutées par Claude Code à partir des liens partagés -->

## Session du 27 février 2026
<!-- source: conversation Claude.ai Jour 4 — NumPy et Pandas -->

**[Question/Sujet]** Pourquoi NumPy est-il plus rapide que Python pur ?

**[Explication]** Python est lent parce que c'est un langage interprété et dynamiquement typé. À chaque opération, Python doit vérifier le type de chaque variable, appeler des couches d'abstraction, gérer la mémoire dynamiquement. Pour une boucle sur 1 million d'éléments, ça fait 1 million de vérifications.

C est rapide parce que c'est compilé et statiquement typé. Les types sont connus à l'avance, le code est traduit directement en instructions CPU. Pas de vérifications à l'exécution.

NumPy est du C déguisé en Python. Quand tu fais `np.sum(array)`, tu n'exécutes pas une boucle Python — tu appelles une fonction compilée en C qui opère directement sur un bloc mémoire contigu. Python n'intervient qu'une seule fois pour lancer l'appel. Le secret : NumPy stocke ses données dans des arrays de type fixe (tous les éléments ont le même type, connu à l'avance).

```python
# Python pur — 1M de vérifications de type
total = sum([x for x in range(1_000_000)])

# NumPy — 1 appel C sur un bloc mémoire
import numpy as np
total = np.sum(np.arange(1_000_000))  # ~100x plus rapide
```

**[Insight clé]** Dès que tu vois une boucle Python sur un array NumPy, c'est un signal d'alarme — tu perds tout le bénéfice de NumPy.

---

**[Question/Sujet]** Typage dynamique vs statique — définition

**[Explication]** En Python, le type d'une variable est déterminé à l'exécution, pas à l'avance :

```python
x = 42        # Python découvre que c'est un int ici
x = "hello"   # maintenant c'est un str — aucun problème
```

En C, tu dois déclarer le type avant :
```c
int x = 42;
x = "hello";  // erreur de compilation — interdit
```

Dynamique = le type est découvert au moment où la ligne s'exécute → overhead à chaque opération. Statique = le type est connu avant même de lancer le programme → le compilateur optimise tout à l'avance.

**[Insight clé]** NumPy contourne le typage dynamique de Python en imposant un `dtype` fixe pour tous les éléments d'un array — c'est la clé du gain de performance.

---

**[Question/Sujet]** np.array vs list Python

**[Explication]**
- `list` Python : peut contenir des types mixtes (`[1, "a", True]`) → Python vérifie chaque élément
- `np.array` : tous les éléments ont le même type (dtype) → connu à l'avance → calcul C direct
- `np.array` supporte les opérations vectorisées : `array * 2` multiplie tous les éléments d'un coup (avec une list, il faudrait une boucle)

**[Insight clé]** Le dtype fixe permet d'éliminer les vérifications de type à chaque élément et de passer le tableau directement au code C.

---

**[Question/Sujet]** Dimensions des arrays NumPy

**[Explication]**
- 1D : vecteur — ex: `[1, 2, 3]`
- 2D : matrice — ex: tableau de données, image en niveaux de gris
- 3D : image couleur (hauteur × largeur × 3 canaux RGB)
- 4D : vidéo couleur (frames × hauteur × largeur × 3 canaux)

**[Insight clé]** Les dimensions correspondent à des cas d'usage réels en data engineering et computer vision.

---

**[Question/Sujet]** Méthodes et attributs essentiels NumPy

**[Explication]**
- `.shape` ← pas de parenthèses, c'est un **attribut**, pas une méthode
- `.dtype` ← type des éléments (float64, int32...)
- `.flatten()` → aplatit en 1D, shape devient `(N,)`
- `.reshape(a, b)` → change la forme sans changer les données (nb d'éléments doit rester identique)
- `.T` → transposée (lignes ↔ colonnes)

Fonctions de création :
- `np.zeros((3, 4))`, `np.ones((3, 4))` — le tuple est requis directement
- `np.eye(N)` → matrice identité N×N (1 sur la diagonale, 0 ailleurs)
- `np.arange(0, 10, 2)` → comme `range()` mais retourne un array
- `np.linspace(0, 10, 5)` → 5 points régulièrement espacés entre 0 et 10 inclus
- `np.random.normal()` → distribution gaussienne (= distribution normale, même chose)

Algèbre linéaire (`np.linalg`) :
- `np.linalg.inv(a)` — inverse, `np.linalg.det(a)` — déterminant, `np.linalg.norm(a)` — norme, `np.linalg.eig(a)` — valeurs propres

**[Insight clé]** Règle : parenthèses = méthode (action), pas de parenthèses = attribut (info). `.shape` sans parenthèses est l'erreur classique.

---

**[Question/Sujet]** Différence entre `np.arange` et `np.linspace`

**[Explication]**
```python
np.arange(0, 10, 2)      # start, stop (exclu), step → [0, 2, 4, 6, 8]
np.linspace(0, 10, 5)    # start, stop (inclus), nb_points → [0., 2.5, 5., 7.5, 10.]
```

Avec `arange` on contrôle le **pas**, avec `linspace` on contrôle le **nombre de points**. Pour des calculs numériques, `linspace` est souvent préférable car il garantit exactement N points sans surprises d'arrondi flottant.

**[Insight clé]** `linspace` pour "je veux N points entre A et B", `arange` pour "je veux compter par pas de X".

---

**[Question/Sujet]** Fonctions NumPy avancées — `np.argsort`, `np.pad`, `np.diag`, `np.tile`, `np.bincount`, `np.nonzero`

**[Explication]**
```python
np.argsort(a)    # indices qui trieraient le tableau : [30,10,20] → [1,2,0]
np.pad(a, n)     # ajoute des valeurs (souvent 0) autour d'un array
np.diag(a)       # 1D → crée matrice avec a sur diagonale ; 2D → extrait la diagonale
np.diagonal(a)   # extrait uniquement la diagonale (read-only, contrairement à np.diag)
np.tile(a, n)    # répète un array n fois : [1,2,3] tile 3 → [1,2,3,1,2,3,1,2,3]
np.bincount(a)   # compte occurrences de chaque entier : [0,1,1,2,3,3,3] → [1,2,1,3]
np.nonzero(a)    # indices des éléments non-nuls — utile pour filtrer ou localiser
```

**[Insight clé]** `np.diag` est polyvalent (crée ET extrait), `np.diagonal` fait uniquement l'extraction.

---

**[Question/Sujet]** `np.pad` avec mode 'minimum' — comment ça marche ?

**[Explication]**
```python
a = [[1, 2], [3, 4]]
np.pad(a, ((3, 2), (2, 3)), 'minimum')
# ((3, 2), (2, 3)) = 3 lignes avant + 2 après, 2 colonnes à gauche + 3 à droite
# 'minimum' = remplir avec le minimum trouvé le long du bord correspondant
```

Étape 1 — padding des colonnes : `[1,2]` → min=1 → `[1,1, 1,2, 1,1,1]` ; `[3,4]` → min=3 → `[3,3, 3,4, 3,3,3]`

Étape 2 — padding des lignes : min entre les deux lignes = `[1,1,1,2,1,1,1]` → toutes les lignes de padding valent ça.

**[Insight clé]** Le 1 domine partout car c'est le minimum global de la matrice. NumPy applique le padding dans l'ordre : colonnes d'abord, lignes ensuite.

---

**[Question/Sujet]** Le slicing en NumPy

**[Explication]**
```python
a[1:4]    # éléments d'index 1 à 3
a[:3]     # du début jusqu'à l'index 2
a[1:-1]   # de l'index 1 jusqu'à l'avant-dernier (exclu)

# En 2D — slicing simultané sur les deux axes :
a[1:4, 2:5]   # lignes 1-3, colonnes 2-4
a[1:-1, 1:-1] # tout sauf la bordure extérieure
```

**[Insight clé]** En 2D, le slicing s'applique simultanément sur les deux axes avec une virgule.

---

**[Question/Sujet]** Exercice : array 10×10 avec 1 sur la bordure et 0 à l'intérieur

**[Explication]** Solution initiale (correcte mais verbeuse) :
```python
f = np.zeros(100).reshape(10, 10)   # reshape inutile ici
f[0:10,0] = np.ones(10)
f[0,0:10] = np.ones(10)
f[0:10,9] = np.ones(10)
f[9,0:10] = np.ones(10)
```

Version optimisée :
```python
f = np.zeros((10, 10))    # tuple directement dans np.zeros
f[[0, -1], :] = 1         # première et dernière ligne
f[:, [0, -1]] = 1         # première et dernière colonne
```

Version la plus compacte avec `np.pad` :
```python
f = np.pad(np.zeros((8, 8)), pad_width=1, constant_values=1)
```

**[Insight clé]** `-1` = dernier élément, marche pour n'importe quelle taille. `= 1` (scalaire) est broadcasté automatiquement sur toute la sélection par NumPy.

---

**[Question/Sujet]** Distribution gaussienne vs distribution normale

**[Explication]** C'est la même chose. "Distribution gaussienne" et "distribution normale" sont deux noms pour le même concept — la courbe en cloche. Gauss est le mathématicien qui l'a formalisée. "Normale" vient du fait qu'elle décrit le comportement "normal" de beaucoup de phénomènes naturels.

Propriétés : symétrique autour de la moyenne, 68% des valeurs dans ±1 écart-type, 95% dans ±2.

**[Insight clé]** `np.random.normal()` génère des données suivant cette distribution.

---

**[Question/Sujet]** Outils notebook Jupyter et grep bash

**[Explication]**
- `!` au début d'une ligne → exécute en bash (ex: `!pip freeze | grep numpy`)
- `display(array)` → affiche l'array formaté (mieux que print pour les matrices)
- `grep` en bash : filtre les **lignes** contenant un pattern (recherche par ligne, pas par mot)
- Un `.ipynb` est un fichier JSON — renommer en `.json` → lisible directement, on voit inputs et outputs

Trouver la version NumPy :
- Dans le notebook : `np.__version__`
- En bash : `pip freeze | grep numpy`

**[Insight clé]** `grep` est une recherche par ligne — il retourne les lignes entières qui contiennent le pattern.

---

**[Question/Sujet]** Rappels OOP Python (dans le contexte NumPy)

**[Explication]**
- **Classe** : le plan/modèle (ex: `np.ndarray`)
- **Objet/instance** : une réalisation concrète de ce plan (ex: ton array spécifique)
- **Attribut** : variable attachée à un objet — pas de parenthèses (ex: `array.shape`)
- **Méthode** : fonction attachée à un objet — avec parenthèses (ex: `array.reshape()`)

**[Insight clé]** Parenthèses = méthode (action), pas de parenthèses = attribut (info).

---
