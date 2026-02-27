# Notes — sql-crud

## Optimiser l'usage BigQuery

### Coûts
- Stockage : quasi gratuit (~$0.02/GB/mois)
- Load / Extract / Copy : gratuit
- Processing (queries) : $5/TB scanné — c'est ici qu'il faut optimiser

### Leviers d'optimisation
- **Quotas** : limiter la consommation au niveau projet ou utilisateur
  → Évite les mauvaises surprises sur la facture
- **Limiter les colonnes** : SELECT * est l'ennemi — BigQuery est colonnaire,
  chaque colonne non sélectionnée = données non scannées = moins cher
- **Partitioning** : découpe la table en fichiers par date (ou autre colonne)
  → Partition pruning = BigQuery ne lit que les fichiers pertinents
- **Clustering** : trie les données à l'intérieur d'une partition par une colonne
  → Permet de sauter des blocs de lignes non pertinents
- **Structs** : regroupement de colonnes liées en un objet imbriqué
  → Réduit la complexité du schéma, améliore la lisibilité
- **Arrays** : stocker plusieurs valeurs dans une seule cellule
  → Réduit la dénormalisation et le stockage

### Contraintes à connaître
- `CREATE OR REPLACE` ne fonctionne qu'au sein d'une même région
  → Si tu veux copier une table EU → US, il faut passer par Export/Import ou Transfer Service

---

## Table vs View

| | Table | View |
|---|---|---|
| Stockage | Octets de données sauvegardés | Aucun stockage — juste une requête sauvegardée |
| Exécution | Données déjà calculées | Recalculée à chaque appel |
| Cas d'usage | Dashboard fréquemment consulté, données finales | Étape intermédiaire de pipeline, proxy de sécurité |
| Coût | Stockage facturé | Processing facturé à chaque appel |
| Sécurité | Accès direct aux données | Peut masquer les tables sources → accès contrôlé |

**Règle de décision** : si la même requête est exécutée souvent → matérialise en table.
Si tu veux contrôler l'accès ou créer une étape intermédiaire → view.

**Materialized View** (bonus) : hybride — résultat pré-calculé comme une table,
mais mis à jour automatiquement quand les données sources changent.

---

## Live Share (VS Code)

- Permet de coder à plusieurs sur le même fichier en temps réel
- Fonctionne bien pour : fichiers `.py`, `.sql`, `.md`
- Fonctionne mal pour : notebooks Jupyter (conflits de cellules)
- Donne accès au terminal de l'hôte → ne partager qu'avec des personnes de confiance
- Alternative plus sûre pour notebooks : Google Colab (collaboration native)
