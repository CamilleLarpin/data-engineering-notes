# Notes — numpy
## Sous le capot
- NumPy s'exécute en C.
- Python est lent : interprété + typage dynamique = vérifications à chaque opération.
- C est rapide : compilé + typage statique = instructions CPU directes.
- NumPy = interface Python + calculs en C sur des arrays à type fixe.
- Gain : types connus à l'avance → pas de vérifications en boucle → ~100x plus rapide que Python pur.

## np.array vs list
- list Python : peut contenir des types mixtes ([1, "a", True]) → Python vérifie chaque élément
- np.array : tous les éléments ont le même type (dtype) → connu à l'avance → calcul C direct
- np.array supporte les opérations vectorisées : array * 2 multiplie tous les éléments d'un coup
  (avec une list, il faudrait une boucle)

## Dimensions
- 1D : vecteur — ex: [1, 2, 3]
- 2D : matrice — ex: tableau de données, image en niveaux de gris
- 3D : image couleur (hauteur × largeur × 3 canaux RGB)
- 4D : vidéo couleur (frames × hauteur × largeur × 3 canaux)

## Méthodes essentielles
- .shape  ← pas de parenthèses, c'est un attribut, pas une méthode
- .dtype  ← affiche le type des éléments (float64, int32...)
- .flatten() → aplatit en 1D, shape devient (N,)
- .reshape(a, b) → change la forme sans changer les données (nb d'éléments doit rester identique)
- .T → transposée (lignes ↔ colonnes)

## Création d'arrays
- np.zeros((3, 4))    → matrice de zéros
- np.ones((3, 4))     → matrice de uns
- np.eye(N)           → matrice identité N×N (1 sur la diagonale, 0 ailleurs)
- np.arange(0, 10, 2) → équivalent de range() mais retourne un array
- np.random.normal()  → distribution gaussienne (= distribution normale, même chose)

## Dans un notebook Jupyter
- ! au début d'une ligne → exécute en bash (ex: !pip freeze | grep numpy)
- display(array) → affiche l'array formaté (mieux que print pour les matrices)

## Trouver la version NumPy
- Dans le notebook : import numpy as np; np.__version__
- En bash : pip freeze | grep numpy
- grep en bash : filtre les lignes contenant un pattern (recherche par ligne, pas par mot)

## Python — rappels OOP
- Classe : le plan/modèle (ex: np.ndarray)
- Objet/instance : une réalisation concrète de ce plan (ex: ton array spécifique)
- Attribut : variable attachée à un objet (ex: array.shape — pas de parenthèses)
- Méthode : fonction attachée à un objet (ex: array.reshape() — avec parenthèses)
  → règle simple : parenthèses = méthode (action), pas de parenthèses = attribut (info)
