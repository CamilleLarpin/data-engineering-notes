# Fiche — sql-crud

---

## Session — 2026-02-25
BigQuery optimization levers, table vs view trade-offs, and project navigation in the GCP console.

### BigQuery console project navigation
The left panel in the BigQuery console is an explorer of pinned projects only, not all active projects. Datasets belonging to a project are only visible in the left panel after the project is starred or pinned. The resource hierarchy is Project → Dataset → Table.

### BigQuery cost model
Storage costs are negligible. Data load, extract, and copy operations are free. Query processing is billed per TB scanned — this is the primary cost lever to optimize.

### Columnar storage and SELECT *
BigQuery uses columnar storage, meaning each column is stored and scanned independently. Selecting only needed columns avoids scanning unused columns entirely, directly reducing query cost.

### Partitioning
Partitioning splits a table into separate physical files based on a column value (commonly a date). At query time, BigQuery applies partition pruning — only the relevant partition files are read, reducing bytes scanned.

### Clustering
Clustering sorts data within a partition by one or more columns. This allows BigQuery to skip entire blocks of rows that do not match a filter predicate, further reducing scan cost within a partition.

### Structs and Arrays
Structs group related columns into a nested object, reducing schema complexity. Arrays store multiple values in a single cell, reducing denormalization and the number of rows needed to represent one-to-many relationships.

### CREATE OR REPLACE cross-region constraint
CREATE OR REPLACE only works within the same GCP region. Copying a table across regions (e.g., EU to US) requires Export/Import or the BigQuery Transfer Service.

### Table vs View
A table stores data physically — query results are precomputed and reads are fast. A view stores only the query definition — it is recomputed on every call, so processing cost is incurred at read time. Views can mask underlying tables to control access. A materialized view is a hybrid: results are precomputed like a table but automatically refreshed when source data changes.
