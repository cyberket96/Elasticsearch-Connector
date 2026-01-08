# CLI

from __future__ import annotations

import json
import os
import warnings

from dotenv import load_dotenv
from elastic_transport import TransportWarning
from tabulate import tabulate
from urllib3.exceptions import InsecureRequestWarning

from features.delete_doc import delete_doc
from features.fetch_health import fetch_health
from features.fetch_indices import fetch_indices
from features.fetch_schema import fetch_schema
from features.ingest_doc import ingest_doc
from features.run_query import run_query
from features.test_connection import test_connection
from features.test_query import test_query

warnings.filterwarnings("ignore", category=TransportWarning)
warnings.filterwarnings("ignore", category=InsecureRequestWarning)


def print_introduction() -> None:
    print("-" * 64)
    print("Elastic Connector — CLI Mode")
    print("-" * 64)
    print("Tips:")
    print("  - Type 'help' to list commands.")
    print("  - Type 'help <command>' for command details.")
    print("  - Type 'exit' to quit.")
    print("-" * 64)


def print_help(command: str | None = None) -> None:
    if not command:
        print("Available commands:")
        print("  - test_connection")
        print("  - fetch_health")
        print("  - fetch_indices")
        print("  - fetch_schema")
        print("  - test_query")
        print("  - run_query")
        print("  - ingest_doc")
        print("  - delete_doc")
        print("  - help [command]")
        print("  - exit")
        print("")
        return

    details = {
        "test_connection": "Validate connectivity/auth to Elasticsearch. Params: none.",
        "fetch_health": "Show cluster health summary. Params: none.",
        "fetch_indices": "List indices (name, health, docs, size). Params: none.",
        "fetch_schema": "Show mapping/schema summary. Params: index_name optional (blank=all).",
        "test_query": "Validate ES|QL executes successfully. Params: esql_query.",
        "run_query": "Run ES|QL and print results as a table. Params: esql_query.",
        "ingest_doc": "Create index if missing + ingest docs. Params: index_name, mapping_file, data_file.",
        "delete_doc": "Delete index or delete-by-query. Params: index_name, mode=index|query, query_json if mode=query.",
        "exit": "Exit the CLI.",
        "help": "Show help. Params: optional command name.",
    }

    msg = details.get(command)
    if not msg:
        print(f"Unknown command '{command}'. Type 'help' to list commands.\n")
        return

    print(f"{command}: {msg}\n")


def _require_env(es_url: str | None, username: str | None, password: str | None) -> bool:
    if not es_url or not username or not password:
        print("Error: Missing Elasticsearch credentials.")
        print("Required environment variables:")
        print("  - ES_URL")
        print("  - ES_USERNAME")
        print("  - ES_PASSWORD")
        print("Fix: set them in your .env file.\n")
        return False
    return True


def _print_error(result: dict) -> None:
    msg = result.get("message", "Unknown error")
    err = result.get("error")

    if isinstance(err, dict):
        err_type = err.get("type")
        details = err.get("details")
        if err_type and details:
            print("Result: FAILED.")
            print(f"  - Message: {msg}")
            print(f"  - Error:   {err_type}")
            print(f"  - Details: {details}\n")
            return
        if err_type:
            print("Result: FAILED.")
            print(f"  - Message: {msg}")
            print(f"  - Error:   {err_type}\n")
            return

    print(f"Result: FAILED.\n  - Message: {msg}\n")


def _render_indices_table(indices: list[dict]) -> None:
    if not indices:
        print("Result: OK.\n  - No indices found.\n")
        return

    headers = ["index", "health", "status", "docs.count", "store.size"]
    rows = [[i.get(h) for h in headers] for i in indices]
    print("Result: OK.\n")
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print("")


def _render_schema_summary(schema: dict, limit_fields: int = 40) -> None:
    if not schema:
        print("Result: OK.\n  - No schema returned.\n")
        return

    for index, payload in schema.items():
        props = (payload.get("mappings") or {}).get("properties") or {}
        print("Result: OK.")
        print(f"  - Index: {index}")
        print(f"  - Top-level fields: {len(props)}")

        if not props:
            print("")
            continue

        rows = []
        for name, details in props.items():
            dtype = (details or {}).get("type", "object")
            rows.append([name, dtype])

        rows = rows[:limit_fields]
        print(tabulate(rows, headers=["field", "type"], tablefmt="grid"))

        if len(props) > limit_fields:
            print(f"... truncated ({len(props) - limit_fields} more fields)")
        print("")


def _render_esql_results(data: dict) -> None:
    if not data:
        print("Result: OK.\n  - No results returned.\n")
        return

    columns = data.get("columns") or []
    values = data.get("values") or []
    headers = [c.get("name") for c in columns] if columns else None

    if not values:
        print("Result: OK.\n  - Query executed successfully (0 rows).\n")
        return

    print("Result: OK.\n")
    print(tabulate(values, headers=headers, tablefmt="grid"))
    print("")


def main() -> None:
    load_dotenv()

    es_url = os.getenv("ES_URL")
    username = os.getenv("ES_USERNAME")
    password = os.getenv("ES_PASSWORD")

    if not _require_env(es_url, username, password):
        return

    print_introduction()

    while True:
        raw = input("> ").strip()
        if not raw:
            continue

        parts = raw.split(maxsplit=1)
        command = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else None

        if command == "help":
            print_help(arg.lower() if arg else None)
            continue

        if command in {"exit", "quit"}:
            print("Goodbye!")
            break

        if command == "test_connection":
            result = test_connection(es_url, username, password)
            if result.get("success"):
                print("Result: OK.\n  - Connection successful.\n")
            else:
                _print_error(result)
            continue

        if command == "fetch_health":
            result = fetch_health(es_url, username, password)
            if result.get("success"):
                h = result.get("data") or {}
                print("Result: OK.")
                print(f"  - status:              {h.get('status')}")
                print(f"  - number_of_nodes:     {h.get('number_of_nodes')}")
                print(f"  - number_of_data_nodes:{h.get('number_of_data_nodes')}")
                print(f"  - active_shards:       {h.get('active_shards')}")
                print(f"  - unassigned_shards:   {h.get('unassigned_shards')}\n")
            else:
                _print_error(result)
            continue

        if command == "fetch_indices":
            result = fetch_indices(es_url, username, password)
            if result.get("success"):
                _render_indices_table(result.get("data") or [])
            else:
                _print_error(result)
            continue

        if command == "fetch_schema":
            index_name = input("index_name (blank=all): ").strip() or None
            result = fetch_schema(es_url, username, password, index_name)
            if result.get("success"):
                _render_schema_summary(result.get("data") or {})
            else:
                _print_error(result)
            continue

        if command == "test_query":
            esql_query = input("esql_query: ").strip()
            result = test_query(es_url, username, password, esql_query)
            if result.get("success"):
                s = result.get("data") or {}
                print("Result: OK.")
                print(f"  - rows:    {s.get('rows_count')}")
                print(f"  - cols:    {s.get('columns_count')}")
                print(f"  - took:    {s.get('took')} ms")
                print(f"  - partial: {s.get('is_partial')}\n")
            else:
                _print_error(result)
            continue

        if command == "run_query":
            esql_query = input("esql_query: ").strip()
            result = run_query(es_url, username, password, esql_query)
            if result.get("success"):
                _render_esql_results(result.get("data") or {})
            else:
                _print_error(result)
            continue

        if command == "ingest_doc":
            index_name = input("index_name: ").strip()
            mapping_file = input("mapping_file (path): ").strip()
            data_file = input("data_file (path): ").strip()

            result = ingest_doc(es_url, username, password, index_name, mapping_file, data_file)
            if result.get("success"):
                info = result.get("data") or {}
                print("Result: OK.")
                print(f"  - index:         {info.get('index')}")
                print(f"  - created_index: {info.get('created_index')}")
                print(f"  - ingested:      {info.get('ingested_docs')}/{info.get('requested_docs')}\n")
            else:
                _print_error(result)
            continue

        if command == "delete_doc":
            index_name = input("index_name: ").strip()
            mode = input("mode (index|query): ").strip().lower()

            if mode == "index":
                result = delete_doc(es_url, username, password, index_name, query=None)
                if result.get("success"):
                    print(f"Result: OK.\n  - {result.get('message')}\n")
                else:
                    _print_error(result)
                continue

            if mode == "query":
                query_str = input('query JSON (e.g., {"match_all":{}}): ').strip()
                try:
                    query = json.loads(query_str)
                except json.JSONDecodeError as exc:
                    print(f"Result: FAILED.\n  - Invalid JSON: {exc}\n")
                    continue

                result = delete_doc(es_url, username, password, index_name, query=query)
                if result.get("success"):
                    info = result.get("data") or {}
                    print("Result: OK.")
                    print(f"  - deleted: {info.get('deleted')}\n")
                else:
                    _print_error(result)
                continue

            print("Result: FAILED.\n  - mode must be 'index' or 'query'.\n")
            continue

        print(f"Result: FAILED.\n  - Unknown command '{command}'. Type 'help'.\n")
