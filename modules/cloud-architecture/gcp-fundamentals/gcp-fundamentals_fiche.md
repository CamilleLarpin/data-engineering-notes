# Fiche — gcp-fundamentals

## 2026-02-24
- BigQuery hierarchy: Project → Dataset → Table (dataset = container defining location/region for tables)
- Dataset creation via UI (learning), bq CLI (scripting), or Python client (production pipelines)
- Region setting is permanent once set on dataset - affects query costs and latency
- `autodetect=True` convenient but risky in production (can miscast types like "01" → 1)
- File transfer to VM: scp command, VS Code drag-drop via Remote SSH, or GCS bucket (production pattern)
- Authentication: `gcloud auth login` for CLI vs `gcloud auth application-default login` for Python applications

---

## Session — 2026-02-24
BigQuery data hierarchy, dataset creation, and CSV/JSON upload via Python client.

### BigQuery Data Hierarchy
Data is organised as Project → Dataset → Table. A dataset is a container for tables and defines the physical storage region (e.g. EU, US). Region is set at dataset creation and cannot be changed afterward. Cross-region queries incur higher latency and cost.

### Uploading Files via Python Client
The `google-cloud-bigquery` Python client supports programmatic dataset creation and file ingestion. `client.create_dataset(dataset, exists_ok=True)` creates a dataset without error if it already exists. `client.load_table_from_file()` with a `LoadJobConfig` handles CSV and newline-delimited JSON. `job.result()` blocks until the load job completes.

### Schema Autodetect Risk
`autodetect=True` infers schema from file contents. It is convenient for exploration but risky in production — it can miscast types (e.g. treating `"01"` as integer, dropping leading zeros). Explicit schema definition is preferred in production pipelines.

### Authentication: Two Separate Credentials
`gcloud auth login` authenticates the user for the `gcloud` CLI. `gcloud auth application-default login` authenticates applications (e.g. Python scripts) running on the user's behalf. Both are required independently. On a GCE VM, a service account is available by default, but it requires explicit BigQuery permissions to be configured.
