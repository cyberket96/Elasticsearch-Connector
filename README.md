# Elasticsearch Connector (CLI)

**A lightweight, detection-centric CLI toolkit for interacting with Elasticsearch.**

The Elasticsearch Connector is a simple, interactive command-line tool designed for detection engineers and platform engineers who need quick, reliable access to Elasticsearch for validation, exploration, and operational tasks.
It provides a focused set of commands to test connectivity, inspect cluster health, explore indices and schemas, execute ES|QL queries, and perform basic data ingestion and deletion.
The tool is intentionally stateless, easy to run locally, and optimized for manual workflows such as detection testing, debugging, and research.
Rather than abstracting Elasticsearch behind heavy services, this connector exposes Elasticsearch capabilities directly through a clean CLI interface.

---

## Features

* **Test Connection**
  Validate Elasticsearch connectivity and authentication using configured credentials.

* **Fetch Cluster Health**
  Retrieve a high-level summary of cluster status, node count, and shard health.

* **List Indices**
  Display all indices available in the connected Elasticsearch cluster.

* **Fetch Index Schema**
  Inspect index mappings and field definitions for one or all indices.

* **Test ES|QL Query**
  Validate that an ES|QL query executes successfully without returning full results.

* **Run ES|QL Query**
  Execute an ES|QL query and display query results directly in the CLI.

* **Ingest Documents**
  Create an index if missing and ingest documents from JSON files.

* **Delete Data**
  Delete an entire index or perform delete-by-query using a JSON query.

---

## High-Level Architecture Overview

```mermaid
flowchart LR
    classDef userStyle fill:#E3F2FD,stroke:#1E88E5;
    classDef cliStyle fill:#E8F5E9,stroke:#43A047;
    classDef coreStyle fill:#FFFDE7,stroke:#F9A825;
    classDef esStyle fill:#FCE4EC,stroke:#D81B60;

    User([User / Engineer]) --> CLI[[CLI Interface]]
    CLI --> Core[Elasticsearch Connector Core]
    Core --> Elasticsearch[(Elasticsearch Cluster)]
    Elasticsearch --> Core
    Core --> CLI

    class User userStyle
    class CLI cliStyle
    class Core coreStyle
    class Elasticsearch esStyle
```

---

## Documentation

For detailed usage and internal flow, refer to the following pages:

* **[Connector Working Diagram](Docs/working-diagram.md)**
  In-depth execution flow of the CLI and feature modules.

* **[CLI Usage Guide](Docs/usage.md)**
  Command reference, examples, and expected behavior.

* **[Configuration Guide](Docs/configuration.md)**
  Environment variables, authentication, and configuration precedence.

---
