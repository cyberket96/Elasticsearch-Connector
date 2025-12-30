# CLI Usage Guide

This document explains how to use the **Elasticsearch Connector CLI** and its supported commands.

The CLI runs in **interactive mode** and accepts one command at a time.

## 1️⃣ Starting the CLI

Ensure configuration is set (see Configuration Guide), then start the CLI:

```bash
python main.py
```

On startup, you will see:

```text
Elastic Connector (CLI)
A lightweight, detection-centric toolkit for interacting with Elasticsearch.
Type 'help' for commands. Type 'exit' to quit.
```

## 2️⃣ Basic CLI Commands

### `help`

Displays all available commands.

```text
help
```

### `exit`

Exits the CLI.

```text
exit
```

## 3️⃣ Connectivity & Health Commands

### `test_connection`

Validates connectivity and authentication with Elasticsearch.

```text
test_connection
```

**Output:**

* Success or failure message

### `fetch_health`

Fetches a high-level summary of cluster health.

```text
fetch_health
```

**Output includes:**

* Cluster status
* Number of nodes
* Data nodes
* Active and unassigned shards

## 4️⃣ Discovery & Inspection Commands

### `fetch_indices`

Lists all indices in the connected cluster.

```text
fetch_indices
```

### `fetch_schema`

Displays index mappings (schemas).

```text
fetch_schema
```

You will be prompted:

```text
index_name (blank for all):
```

* Press **Enter** to fetch schemas for all indices
* Provide an index name to fetch a specific schema

## 5️⃣ Query Execution Commands

### `test_query`

Validates that an ES|QL query executes successfully.

```text
test_query
```

Prompt:

```text
esql_query:
```

This command does **not** return query results — it only validates execution.

### `run_query`

Executes an ES|QL query and prints results.

```text
run_query
```

Prompt:

```text
esql_query:
```

## 6️⃣ Data Management Commands

### `ingest_doc`

Creates an index if missing and ingests documents from JSON files.

```text
ingest_doc
```

Prompts:

```text
index_name:
mapping_file (path):
data_file (path):
```

* `mapping_file` → JSON file containing index mappings
* `data_file` → JSON file containing documents to ingest

### `delete_doc`

Deletes data from Elasticsearch.

```text
delete_doc
```

Prompts:

```text
index_name:
mode (index|query):
```

#### Delete entire index

```text
mode: index
```

#### Delete by query

```text
mode: query
query JSON (e.g., {"match_all":{}}):
```

The query must be valid JSON.

---

## 7️⃣ Error Handling Behavior

* Unknown commands display an error message
* Missing inputs are validated before execution
* Invalid JSON input is rejected with a clear error
* Elasticsearch errors are returned as user-readable messages

Example:

```text
Error: Unknown command 'foo'. Type 'help' for a list of available commands.
```

---

## 8️⃣ Usage Notes & Limitations

* Commands are executed sequentially
* One Elasticsearch cluster per session
* No command history or auto-complete
* Designed for **manual, interactive workflows**

These constraints are intentional to keep the CLI lightweight.

---
