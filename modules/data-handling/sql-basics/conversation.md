# Conversations — sql-basics

<!-- Entrées ajoutées par Claude Code à partir des liens partagés -->

## Session du 24 février 2026
<!-- source: (pasted) -->

**[Question/Sujet]** Fonctions de date dans BigQuery — extraire, formater, filtrer

**[Explication]**

**Extraire mois-année (MM-YY) depuis une date** :
```sql
FORMAT_DATE('%m-%y', date_column)
-- ex : '2023-07-15' → '07-23'
```

Codes de format utiles :
- `%Y` → 2023 | `%y` → 23
- `%m` → 07 | `%d` → 15
- `%B` → July | `%b` → Jul (abrégé)

**Filtrer par date** :
```sql
-- Date exacte
WHERE date_column = '2023-07-15'

-- Range
WHERE date_column BETWEEN '2023-01-01' AND '2023-12-31'

-- Par mois/année (moins efficace)
WHERE EXTRACT(YEAR FROM date_column) = 2023
  AND EXTRACT(MONTH FROM date_column) = 7

-- Optimal sur tables partitionnées
WHERE date_column >= '2023-07-01' AND date_column < '2023-08-01'
```

**Performance** : `EXTRACT` et `FORMAT_DATE` sur grandes tables forcent un full scan — ils ne peuvent pas utiliser le partition pruning. Les comparaisons directes (`>=`, `<`) permettent à BigQuery de sauter des partitions entières — beaucoup moins cher à l'échelle.

**Formater une somme avec 2 décimales, signe $, trunckée** :
```sql
SELECT FORMAT('$%.2f', TRUNC(SUM(amount), 2))
-- → '$1234.56'
```

- `TRUNC(x, 2)` → coupe à 2 décimales **sans arrondir** (ex: 1.999 → 1.99)
- `ROUND(x, 2)` → arrondit (ex: 1.999 → 2.00)
- `FORMAT('$%.2f', x)` → formate en string avec $ et 2 décimales (`%.2f` : `f` = float, `.2` = 2 décimales)

Note : `FORMAT()` retourne une **string**, pas un nombre — non utilisable pour des calculs ensuite. Si tu as besoin de continuer à calculer, utiliser `ROUND`.

**Extraire les saisons** (pas de fonction native en BigQuery — hémisphère-dépendant) :
```sql
CASE
  WHEN EXTRACT(MONTH FROM date_column) IN (12, 1, 2)  THEN 'Winter'
  WHEN EXTRACT(MONTH FROM date_column) IN (3, 4, 5)   THEN 'Spring'
  WHEN EXTRACT(MONTH FROM date_column) IN (6, 7, 8)   THEN 'Summer'
  WHEN EXTRACT(MONTH FROM date_column) IN (9, 10, 11) THEN 'Fall'
END AS season
```

`CASE WHEN` en SQL = équivalent de `if/elif` en Python (ou du dict as switch pour des valeurs discrètes).

**[Insight clé]** Toujours filtrer par comparaison directe de dates (`>=`, `<`) sur les grandes tables partitionnées — c'est la seule façon d'activer le partition pruning et d'éviter des scans complets coûteux.

---
