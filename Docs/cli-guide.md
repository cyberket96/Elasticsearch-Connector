# CLI Guide — Elasticsearch Connector

This guide explains how to use the **interactive CLI** for Elasticsearch Connector.  
Start the tool once, then run commands in a continuous prompt until you exit.

---

## 1. Start the CLI

From the project root:

```bash
source .venv/bin/activate
python3 main.py
```

You should see a prompt like:

```text
>
```

---

## 2. Basic Commands

### `help`
Shows a short list of available commands.

```text
> help
```

### `exit`
Closes the CLI cleanly.

```text
> exit
```

---

## 3. Cluster & Data Commands

### `test_connection`
Checks whether Elastic Connector can reach Elasticsearch using the credentials in `.env`.

```text
> test_connection
```

### `fetch_health`
Shows a short cluster health summary (status, nodes, shards).

```text
> fetch_health
```

### `fetch_indices`
Lists indices available in the cluster.

```text
> fetch_indices
```

### `fetch_schema`
Shows mapping/schema details. You can provide an index name/pattern or leave blank for all.

```text
> fetch_schema
index_name (blank=all): logs-*
```

---

## 4. ES|QL Query Commands

### `test_query`
Validates whether an ES|QL query executes successfully.
- This is intended for “does it run?” validation (syntax / fields / compatibility).
- It does not need to print results.

```text
> test_query
esql_query: FROM logs-* | LIMIT 1
```

### `run_query`
Executes an ES|QL query and prints results (table output).

```text
> run_query
esql_query: FROM logs-* | WHERE event.dataset == "elastic_agent" | LIMIT 5
```

---

## 5. Scenario / Telemetry Commands

These are useful for **detection validation workflows** (ingest test logs → run query/detection → cleanup).

### `ingest_doc`
Ingests JSON docs into an index. Prompts:
- `index_name`
- `mapping_file` (path to mapping JSON)
- `data_file` (path to docs JSON)

Behavior:
- If the index does not exist, it is created using the mapping file.
- Each document gets an `@timestamp` within the last 15 minutes (to simplify time-based searches).

```text
> ingest_doc
index_name: scenario-process-001
mapping_file: ./scenarios/process/mapping.json
data_file: ./scenarios/process/logs.json
```

### `delete_doc`
Deletes data either by deleting the entire index or by using delete-by-query.

You will be asked for:
- `index_name`
- `mode (index|query)`

**Delete entire index**
```text
> delete_doc
index_name: scenario-process-001
mode (index|query): index
```

**Delete documents by query**
Provide a Query DSL JSON (example deletes all docs):
```text
> delete_doc
index_name: scenario-process-001
mode (index|query): query
query JSON (e.g., {"match_all":{}}): {"match_all":{}}
```

---

## 6. Examples

### Example A: Quick cluster check
```text
> test_connection
> fetch_health
> fetch_indices
```

### Example B: Validate an ES|QL query (no results needed)
```text
> test_query
esql_query: FROM logs-* | WHERE host.name IS NOT NULL | LIMIT 1
```

### Example C: Run an ES|QL query and view output
```text
> run_query
esql_query: FROM logs-* | STATS count(*) BY event.dataset | SORT count(*) DESC | LIMIT 10
```

### Example D: Scenario workflow (ingest → run → cleanup)
```text
> ingest_doc
index_name: scenario-auth-001
mapping_file: ./scenarios/auth/mapping.json
data_file: ./scenarios/auth/logs.json

> run_query
esql_query: FROM scenario-auth-001 | LIMIT 5

> delete_doc
index_name: scenario-auth-001
mode (index|query): index
```

---

## Notes

- Elasticsearch connection details are loaded from `.env` (`ES_URL`, `ES_USERNAME`, `ES_PASSWORD`).
- If you see no results when running queries, verify:
  - the index exists,
  - fields referenced in the query exist in the mapping,
  - your time range filters (if any) match the ingested timestamps.
