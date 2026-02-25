# Conversations — sql-advanced

<!-- Entrées ajoutées par Claude Code à partir des liens partagés -->

## Session du 24 février 2026
<!-- source: (pasted) -->

**[Question/Sujet]** Retrouver des queries non sauvegardées dans BigQuery via `INFORMATION_SCHEMA.JOBS`

**[Explication]**
BigQuery logue automatiquement toutes les jobs exécutées, qu'elles soient sauvegardées ou non. On les retrouve via `INFORMATION_SCHEMA.JOBS` :

```sql
SELECT
  creation_time,
  query,
  job_id,
  user_email
FROM `region-eu`.INFORMATION_SCHEMA.JOBS
WHERE job_type = 'QUERY'
  AND user_email = 'ton.email@domain.com'
  AND creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY creation_time DESC
LIMIT 50;
```

Points clés :
- Historique conservé **30 jours** par défaut
- Nécessite la permission `bigquery.jobs.list` (ou `bigquery.jobs.listAll` pour voir les jobs des autres)
- La **région** dans le FROM doit correspondre à celle du projet (`region-eu`, `region-us`, etc.)
- Aussi accessible sans SQL : BigQuery Console → **Historique des jobs**
- Limite : si la query a échoué **avant** d'être soumise (erreur de syntaxe côté client), elle ne sera pas loggée

`TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)` = soustraire 7 jours au timestamp courant — pattern standard pour filtrer sur une fenêtre glissante.

**[Insight clé]** `INFORMATION_SCHEMA` dans BigQuery est une meta-base qui expose les métadonnées du projet (jobs, tables, schémas, etc.). Utile autant pour retrouver du travail perdu que pour auditer les coûts et la performance des queries.

---
