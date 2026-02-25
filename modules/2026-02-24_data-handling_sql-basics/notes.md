# Notes — sql-basics

## SQL Basics

In Case when, there is no need to specify the exclusion of the condition in the lines above. 

```
SELECT
  title,
  NumberPages,
  CASE
    WHEN NumberPages < 30 THEN 'Rapide à lire'
    WHEN NumberPages < 60 THEN 'OK à lire'
    ELSE 'Long à lire'
    END AS IsEasyToRead
FROM `asod-414116.sql_lectures.library`
;

```

## CAST VS SAFE_CAST

- `CAST` >> error if mal functioning
- `SAFE_CAST` >> NULL if mal functioning


`CONCAT(FirstName,LastName)`peut s’écrire `FirstName I I LastName`

`COUNT(1)` :  compte les lignes de la table