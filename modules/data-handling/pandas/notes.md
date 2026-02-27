# Notes — pandas

Limitte pandas gros volume de données (combien exactement?)

les objets importants:
- df.index
- df.columns
- df.info()
- df.describe()
- df.head()

pd.read_XXX("path", sep=",')

language typé: variable a un type definis - float/string etc ... ?

Si on renomme un notebook en plein json - on obtiens un json lisible avec input et output

## Limites de Pandas
- Conçu pour tenir en RAM : règle pratique → max ~1-2x ta RAM disponible
- Sur une machine standard (16GB RAM) : ~5-10GB de données max confortablement
- Au-delà → utiliser Spark, Dask, ou BigQuery directement
- Pandas charge TOUT en mémoire d'un coup (contrairement à SQL qui streame)

## Objets / attributs essentiels
- df.index    → étiquettes des lignes (par défaut 0, 1, 2...)
- df.columns  → noms des colonnes (Index object, itérable)
- df.shape    → (nb_lignes, nb_colonnes) — attribut, pas de parenthèses
- df.dtypes   → type de chaque colonne

## Méthodes d'exploration
- df.info()      → résumé : types, nb valeurs non-nulles, mémoire utilisée
- df.describe()  → stats descriptives (mean, std, min, max, quartiles)
                   → par défaut sur colonnes numériques uniquement
                   → df.describe(include='all') pour inclure les strings
- df.head(n)     → 5 premières lignes par défaut, n si spécifié
- df.tail(n)     → n dernières lignes
- df.sample(n)   → n lignes aléatoires — utile pour explorer sans biais

## Lecture de fichiers
- pd.read_csv("path", sep=",")     → CSV (sep=";" pour fichiers français)
- pd.read_json("path")             → JSON
- pd.read_excel("path")            → Excel
- pd.read_parquet("path")          → Parquet (format colonnaire, très utilisé en DE)
- pd.read_sql("SELECT...", conn)   → depuis une base SQL

## Sélection
- df["colonne"]          → Series (une colonne)
- df[["col1", "col2"]]  → DataFrame (plusieurs colonnes)
- df.loc[ligne, col]     → sélection par label
- df.iloc[0, 1]          → sélection par position (index numérique)

## Typage en Pandas
- Pandas infère les types à la lecture (comme Python : typage dynamique)
- Types courants : int64, float64, object (= string), bool, datetime64
- Forcer un type : df["col"].astype(float)
- object vs string : "object" est le type Pandas legacy pour les strings
  → pd.StringDtype() est le type moderne mais moins répandu

## Notebooks Jupyter — structure JSON
- Un .ipynb est un fichier JSON : cells[], metadata, outputs[]
- Renommer en .json → lisible directement, on voit inputs et outputs séparément
- Utile pour débugger, versionner proprement avec git (git diff lisible)
- Bonne pratique git : toujours Clear All Outputs avant de committer
  → évite les diffs illisibles sur les outputs

## Checker nb de valeurs manquantes par colonnes
- df.isna().sum()
- df.isnull().sum()