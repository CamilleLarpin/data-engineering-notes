
<!-- from: data-handling/sql-crud -->
# Conversations — sql-crud

<!-- Entrées ajoutées par Claude Code à partir des liens partagés -->

## Session du 27 février 2026
<!-- source: conversation Claude.ai Jour 4 — NumPy et Pandas -->

**[Question/Sujet]** Différence entre Partitioning et Clustering en BigQuery

**[Explication]** Pense à une grande bibliothèque de livres.

**Partitioning** = découper physiquement la table en fichiers séparés selon une colonne (souvent une date). Quand tu filtres sur cette colonne, BigQuery ne lit littéralement pas les autres fichiers. C'est du pruning physique — les données ne sont jamais chargées.

```sql
WHERE date_col >= '2024-03-01'  -- BigQuery ne lit que le fichier "mars 2024"
```

**Clustering** = à l'intérieur de chaque partition (ou de la table entière), BigQuery trie et regroupe les lignes par une ou plusieurs colonnes. Quand tu filtres sur une colonne clusterisée, BigQuery peut sauter des blocs de lignes non pertinents. C'est du pruning logique à l'intérieur d'un fichier.

Analogie : partitioning = des tiroirs séparés par année. Clustering = à l'intérieur de chaque tiroir, les dossiers sont triés par client. Tu cherches "mars 2024, client Akeneo" → tu ouvres le bon tiroir (partition) et tu sautes directement à la bonne section (cluster).

**[Insight clé]** Partitionner par une colonne ne restreint rien — tu peux toujours filtrer sur n'importe quelle autre colonne. C'est juste que BigQuery sera obligé de scanner toutes les partitions si ton filtre ne porte pas sur la colonne de partition → plus de données lues, donc plus cher. La colonne de partition est une **optimisation conditionnelle**, pas une contrainte.

---

**[Question/Sujet]** Modèle de coûts BigQuery et leviers d'optimisation

**[Explication]**

| Opération | Coût |
|-----------|------|
| Stockage | ~$0.02/GB/mois — quasi gratuit |
| Load / Extract / Copy | Gratuit |
| Processing (queries) | $5/TB scanné — à optimiser |

Leviers d'optimisation :
- **Quotas** : limiter la consommation au niveau projet ou utilisateur
- **Limiter les colonnes** : `SELECT *` est l'ennemi — BigQuery est colonnaire, chaque colonne non sélectionnée = données non scannées = moins cher
- **Partitioning** : pruning physique par fichier
- **Clustering** : pruning logique à l'intérieur d'un fichier
- **Structs** : regroupement de colonnes liées en objet imbriqué — réduit la complexité du schéma
- **Arrays** : plusieurs valeurs dans une cellule — réduit la dénormalisation et le stockage

Contrainte à connaître : `CREATE OR REPLACE` ne fonctionne qu'au sein d'une même région. Pour copier EU → US, passer par Export/Import ou Transfer Service.

**[Insight clé]** Le coût est sur le processing, pas le stockage. Optimiser = réduire les données scannées.

---

**[Question/Sujet]** Table vs View en BigQuery — comparaison et cas d'usage

**[Explication]**

| | Table | View |
|---|---|---|
| Stockage | Octets de données sauvegardés | Aucun stockage — juste une requête sauvegardée |
| Exécution | Données déjà calculées | Recalculée à chaque appel |
| Cas d'usage | Dashboard fréquemment consulté, données finales | Étape intermédiaire de pipeline, proxy de sécurité |
| Coût | Stockage facturé | Processing facturé à chaque appel |
| Sécurité | Accès direct aux données | Peut masquer les tables sources → accès contrôlé |

Règle de décision : si la même requête est exécutée souvent → matérialise en table. Si tu veux contrôler l'accès ou créer une étape intermédiaire → view.

**Materialized View** (bonus) : hybride — résultat pré-calculé comme une table, mais mis à jour automatiquement quand les données sources changent.

**[Insight clé]** La View comme proxy de sécurité est un cas d'usage important : elle donne accès à une projection des données sans exposer les tables sources directement.

---

<!-- from: data-handling/sql-advanced -->
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
