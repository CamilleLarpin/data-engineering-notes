# Conversations — gcp-fundamentals

<!-- Entrées ajoutées par Claude Code à partir des liens partagés -->

## Session du 24 février 2026
<!-- source: (pasted) -->

**[Question/Sujet]** Créer un dataset BigQuery et uploader des fichiers CSV/JSON via Python

**[Explication]**
Hiérarchie BigQuery :
```
Project  →  Dataset  →  Table
(serveur)   (schéma)    (table)
```
Un dataset est un conteneur pour tables — il définit aussi la **région** (EU, US), qui impacte latence et coûts. La région est fixée à la création et ne peut pas être changée.

3 méthodes d'upload :

| Méthode | Idéale pour |
|---|---|
| BigQuery UI (Console) | Apprentissage, one-off |
| bq CLI | Scripts, automation |
| Python client (google-cloud-bigquery) | Pipelines, contrôle programmatique |

**Via Python (pattern production)** :
```python
from google.cloud import bigquery

client = bigquery.Client(project="your-project-id")

# Créer dataset
dataset = bigquery.Dataset("your-project-id.your_dataset")
dataset.location = "EU"
client.create_dataset(dataset, exists_ok=True)

# Uploader 4 fichiers en boucle
files = {
    "items": "items.csv",
    "stores": "stores.csv",
    "vendors": "vendors.csv",
    "transactions": "transactions.json",
}

job_config = bigquery.LoadJobConfig(autodetect=True)

for table_name, filepath in files.items():
    job_config.source_format = (
        bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        if filepath.endswith(".json")
        else bigquery.SourceFormat.CSV
    )
    with open(filepath, "rb") as f:
        job = client.load_table_from_file(
            f, f"your-project-id.your_dataset.{table_name}", job_config=job_config
        )
    job.result()  # attend la complétion
    print(f"Loaded {table_name} ✅")
```

Note : `open()` en Python n'expand pas `~` comme le shell — utiliser des chemins relatifs si on run depuis le dossier des données.

`autodetect=True` est pratique mais risqué en production : peut mal caster des types (ex : "01" comme integer, dropping le zéro). En vrai pipeline → définir le schéma explicitement.

**[Insight clé]** Penser en boucle dict sur les fichiers évite de répéter 4 fois le même code — pattern standard en Data Engineering.

---

**[Question/Sujet]** Authentification GCP pour les scripts Python

**[Explication]**
Deux commandes d'auth distinctes :

| Commande | Pour qui |
|---|---|
| `gcloud auth login` | Toi, en CLI |
| `gcloud auth application-default login` | Tes applications Python |

Sans `application-default login`, le client Python BigQuery lève une erreur `403 ACCESS_TOKEN_SCOPE_INSUFFICIENT`.

```bash
gcloud auth application-default login
```

Sur une VM GCP, un warning apparaît : "la VM a déjà des credentials de service account, es-tu sûr ?" → Taper Y pour le contexte d'apprentissage. En production, on configurerait le service account proprement.

**[Insight clé]** Un badge pour toi entrer dans le bâtiment (`gcloud auth login`), un autre badge pour ton robot assistant accéder au classeur (`application-default login`).

---

**[Question/Sujet]** Transférer des fichiers de son ordi local vers la VM GCP

**[Explication]**
3 options :

**Option 1 — `scp` (terminal, one-off)** :
```bash
# Depuis ton terminal LOCAL :
scp -i ~/.ssh/id_rsa /path/to/file.csv username@external_ip:~/destination/

# Dossier entier :
scp -i ~/.ssh/id_rsa -r /path/to/folder/ username@external_ip:~/
```

**Option 2 — VS Code drag & drop** (le plus simple pour quelques fichiers) : ouvrir Remote SSH Explorer dans VS Code → glisser les fichiers depuis Finder vers l'arborescence VS Code.

**Option 3 — Google Cloud Storage** (pattern production) :
```bash
gsutil cp gs://your-bucket/file.csv ~/destination/
```
C'est le pattern Data Engineering standard — VM ↔ GCS plutôt que local ↔ VM.

Pour quelques fichiers en apprentissage → Option 2. Pour des pipelines → Option 3.

**[Insight clé]** En Data Engineering, les données transitent via GCS, pas directement entre local et VM. GCS est la "zone de transit" standard.

---

## Session du 24 février 2026 — Historique des jobs
<!-- source: (pasted) -->

**[Question/Sujet]** Retrouver des queries non sauvegardées dans BigQuery

**[Explication]**
BigQuery logue toutes les jobs exécutées automatiquement. Retrouver via `INFORMATION_SCHEMA.JOBS` ou dans la Console (Historique des jobs).

- Historique conservé **30 jours** par défaut
- Nécessite `bigquery.jobs.list` (ou `bigquery.jobs.listAll` pour les jobs des autres)
- La région dans le FROM doit correspondre à celle du projet (`region-eu`, `region-us`)
- Limite : si la query a échoué avant d'être soumise (erreur client), elle ne sera pas loggée

**[Insight clé]** `INFORMATION_SCHEMA` expose les métadonnées du projet — utile pour retrouver du travail perdu, auditer les coûts et la performance. Voir `sql-advanced/conversation.md` pour la query complète.

---
