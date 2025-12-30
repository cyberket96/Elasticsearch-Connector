# Connector Features

This page provides the overview of the elasticsearch connector features/capability.

## Test Connection (test-connection)

- Elasticsearch API: GET _cluster/health
- Elasticsearch PyClient Function: client.cluster.health()

This feature validates the connection to an Elasticsearch cluster using the provided host and authentication details. It confirms whether the cluster is reachable and returns clear error messages when authentication or network failures occur.

## Fetch indices (fetch-indices)

- Elasticsearch API: GET _cat/indices
- Elasticsearch PyClient Function: client.cat.indices()

This feature fetches a list of all indices (sources) from the connected Elasticsearch cluster. It helps users explore available data sources for querying, ingestion, and schema analysis.

## Fetch Schema (fetch-schema)

- Elasticsearch API: GET _mapping
- Elasticsearch PyClient Function: client.indices.get_mapping()

This feature retrieves the schema/mappings for a specified index. It helps users understand field types, structures, and nested objects to build accurate queries and detection logic.

## Fetch Health (fetch-health)

- Elasticsearch API: GET _cluster/health
- Elasticsearch PyClient Function: client.cluster.health()

This feature provides the health status of the Elasticsearch cluster, including overall health (green/yellow/red), node availability, and any reported issues. Useful for monitoring and troubleshooting cluster conditions.

## Test Query (test-query)

- Elasticsearch API: POST /_query
- Elasticsearch PyClient Function: client.esql.query()

This feature lets users run a predefined or simple test query against an index to validate that queries are working as expected. It helps verify the structure, syntax, and performance of basic queries.

## Run Query (run-query)

- Elasticsearch API: POST /_query
- Elasticsearch PyClient Function: client.esql.query()

This feature allows users to run any custom Elasticsearch query. It supports flexible testing, debugging, and exploration of data without predefined constraints, returning raw or formatted query results.

## Ingest Document (ingest-doc)

- Elasticsearch API: POST /{index}/_bulk
- Elasticsearch PyClient Function: bulk() / client.indices.create() / client.indices.exists

This feature enables users to ingest documents into a specified Elasticsearch index. It supports input validation, custom IDs, and error handling to ensure reliable and controlled data ingestion.

## Delete Document (delete-doc)

- Elasticsearch API: POST /{index}/_delete_by_query
- Elasticsearch PyClient Function: delete_by_query() / client.indices.delete()

This feature allows users to delete a document by ID from a selected index. It ensures safe deletion with clear responses about success, failures, or missing documents.

---
