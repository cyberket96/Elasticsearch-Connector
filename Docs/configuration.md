# Configuration Guide

This document explains how to configure the Elasticsearch Connector CLI to connect to an Elasticsearch cluster.

---

## Configuration Overview

The connector uses **environment variables** for configuration.
All required values are loaded at runtime from a `.env` file or the system environment.

There is **no dynamic or runtime configuration** beyond these values.

## Required Environment Variables

The following variables **must be set** before running the CLI:

| Variable      | Description                                               |
| ------------- | --------------------------------------------------------- |
| `ES_URL`      | Elasticsearch cluster URL (e.g. `https://localhost:9200`) |
| `ES_USERNAME` | Username for authentication                               |
| `ES_PASSWORD` | Password for authentication                               |

If any of these values are missing, the connector will not start.

### Using a `.env` File (Recommended)

The easiest way to configure the connector is using a `.env` file in the project root.

#### Example `.env`

```env
ES_URL=https://localhost:9200
ES_USERNAME=elastic
ES_PASSWORD=changeme
```

The CLI automatically loads this file at startup.

### Configuration Validation

At startup, the connector validates that all required variables are present.

If validation fails, the CLI exits with an error message:

```text
Error: Missing Elasticsearch credentials.
Set ES_URL, ES_USERNAME, ES_PASSWORD in .env.
```

No partial execution is allowed without valid configuration.

## SSL & Certificate Warnings

The connector suppresses SSL-related warnings when connecting to Elasticsearch (for example, self-signed certificates).

This behavior is intentional to support **local development and testing environments**.

> ⚠️ This does not disable SSL verification — it only suppresses warning output.

## Configuration Scope & Limitations

* Configuration applies globally for the entire CLI session
* Multiple clusters are not supported in a single run
* Dynamic credential switching is not supported

These limitations are intentional to keep the tool simple.

---
