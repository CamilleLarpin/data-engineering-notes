# Conversations — pandas

<!-- Entrées ajoutées par Claude Code à partir des liens partagés -->

## Session du 27 février 2026
<!-- source: conversation Claude.ai Jour 4 — NumPy et Pandas -->

**[Question/Sujet]** Limites de Pandas et alternatives pour les gros volumes

**[Explication]** Pandas charge TOUT en mémoire d'un coup (contrairement à SQL qui streame). Règle pratique : max ~1-2x ta RAM disponible. Sur une machine standard (16GB RAM) : ~5-10GB de données max confortablement. Au-delà → utiliser Spark, Dask, ou BigQuery directement.

**[Insight clé]** Dès que les données dépassent la RAM, Pandas ne peut plus les gérer — c'est exactement pour ça qu'on verra Spark plus tard.

---

**[Question/Sujet]** Objets, attributs et méthodes essentiels Pandas

**[Explication]** Attributs (pas de parenthèses) :
- `df.index` → étiquettes des lignes (par défaut 0, 1, 2...)
- `df.columns` → noms des colonnes (Index object, itérable)
- `df.shape` → (nb_lignes, nb_colonnes)
- `df.dtypes` → type de chaque colonne

Méthodes d'exploration :
- `df.info()` → résumé : types, nb valeurs non-nulles, mémoire utilisée
- `df.describe()` → stats descriptives (mean, std, min, max, quartiles) — numérique uniquement par défaut ; `df.describe(include='all')` pour inclure les strings
- `df.head(n)` → 5 premières lignes par défaut
- `df.tail(n)`, `df.sample(n)` → fin / lignes aléatoires (utile pour explorer sans biais)

Lecture de fichiers :
```python
pd.read_csv("path", sep=",")    # sep=";" pour fichiers français
pd.read_json("path")
pd.read_excel("path")
pd.read_parquet("path")         # format colonnaire, très utilisé en DE
pd.read_sql("SELECT...", conn)
```

Sélection :
```python
df["col"]            # Series (une colonne)
df[["col1", "col2"]] # DataFrame (plusieurs colonnes)
df.loc[ligne, col]   # par label
df.iloc[0, 1]        # par position (index numérique)
```

**[Insight clé]** `object` est le type Pandas legacy pour les strings. `pd.StringDtype()` est le type moderne mais moins répandu.

---

**[Question/Sujet]** Valeurs distinctes par colonne (non-numériques uniquement)

**[Explication]**
```python
# Une colonne
df["col"].unique()    # array des valeurs distinctes
df["col"].nunique()   # nombre de valeurs distinctes

# Toutes colonnes non-numériques
df.select_dtypes(exclude='number').apply(lambda x: x.unique())
```

`select_dtypes(exclude='number')` garde uniquement les colonnes non-numériques (object, bool, datetime...).

**[Insight clé]** `unique()` retourne les valeurs, `nunique()` retourne le compte.

---

**[Question/Sujet]** Remplacer les données manquantes codées comme '?' par NaN

**[Explication]** Erreurs classiques à éviter :
1. `'np.nan'` (string) ≠ `np.nan` (valeur NaN réelle)
2. `.replace()` ne modifie pas le DataFrame en place — il faut assigner le résultat ou utiliser `inplace=True`

Bonne pratique :
```python
# Remplace dans tout le DataFrame
df.replace('?', np.nan, inplace=True)

# Ou : assigner le résultat
df = df.replace('?', np.nan)
```

**[Insight clé]** `np.nan` sans guillemets. Ne jamais oublier `inplace=True` ou l'assignation — sinon le DataFrame n'est pas modifié.

---

**[Question/Sujet]** Structure JSON d'un notebook Jupyter

**[Explication]** Un `.ipynb` est un fichier JSON : `cells[]`, `metadata`, `outputs[]`. Renommer en `.json` → lisible directement, on voit inputs et outputs séparément. Utile pour débugger ou comprendre la structure.

Bonne pratique git : toujours Clear All Outputs avant de committer → évite les diffs illisibles sur les outputs.

**[Insight clé]** Le notebook est du JSON — ce qui explique pourquoi les conflits git sur les notebooks sont si pénibles.

---
