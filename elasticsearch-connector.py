# Elasticsearch Connector CLI

import json
import os
import warnings
from dotenv import load_dotenv
from elastic_transport import TransportWarning
from urllib3.exceptions import InsecureRequestWarning

from features.test_connection import test_connection
from features.fetch_health import fetch_health
from features.fetch_indices import fetch_indices
from features.fetch_schema import fetch_schema
from features.test_query import test_query
from features.run_query import run_query
from features.ingest_doc import ingest_doc
from features.delete_doc import delete_doc

warnings.filterwarnings("ignore", category=TransportWarning)
warnings.filterwarnings("ignore", category=InsecureRequestWarning)


def print_introduction() -> None:

    print("Elastic Connector (CLI)")
    print("A lightweight, detection-centric toolkit for interacting with Elasticsearch.")
    print("Type 'help' for commands. Type 'exit' to quit.\n")


def print_help() -> None:
    
    lines = [
        "help            : Show this help (none)",
        "exit            : Exit Elastic Connector (none)",
        "test_connection : Validate connectivity/auth to Elasticsearch (none)",
        "fetch_health    : Fetch cluster health summary (none)",
        "fetch_indices   : List indices in the cluster (none)",
        "fetch_schema    : Show index mapping/schema (index_name optional; blank=all)",
        "test_query      : Validate an ES|QL query executes (esql_query)",
        "run_query       : Run an ES|QL query and print results (esql_query)",
        "ingest_doc      : Create index if missing + ingest docs from JSON (index_name, mapping_file, data_file)",
        "delete_doc      : Delete entire index or delete-by-query (index_name, mode=index|query, query_json if mode=query)",
    ]
    print("\n".join(lines) + "\n")


def _require_env(es_url: str | None, username: str | None, password: str | None) -> bool:

    if not es_url or not username or not password:
        print("Error: Missing Elasticsearch credentials. Set ES_URL, ES_USERNAME, ES_PASSWORD in .env.")
        return False
    return True


def main() -> None:

    load_dotenv()

    es_url = os.getenv("ES_URL")
    username = os.getenv("ES_USERNAME")
    password = os.getenv("ES_PASSWORD")

    if not _require_env(es_url, username, password):
        return

    print_introduction()

    while True:
        command = input("> ").strip().lower()

        if not command:
            continue

        if command == "help":
            print_help()
            continue

        if command == "exit":
            print("Goodbye!")
            break

        if command == "test_connection":
            result = test_connection(es_url, username, password)
            print(result["message"])
            continue

        if command == "fetch_health":
            result = fetch_health(es_url, username, password)
            if result["success"]:
                h = result.get("health", {})
                print(
                    "Cluster health: "
                    f"status={h.get('status')}, "
                    f"nodes={h.get('number_of_nodes')}, "
                    f"data_nodes={h.get('number_of_data_nodes')}, "
                    f"active_shards={h.get('active_shards')}, "
                    f"unassigned_shards={h.get('unassigned_shards')}"
                )
            else:
                print(f"Error: {result['message']}")
            continue

        if command == "fetch_indices":
            result = fetch_indices(es_url, username, password)
            if not result["success"]:
                print(f"Error: {result['message']}")
            continue

        if command == "fetch_schema":
            index_name = input("index_name (blank for all): ").strip() or None
            result = fetch_schema(es_url, username, password, index_name)
            if not result["success"]:
                print(f"Error: {result['message']}")
            continue

        if command == "test_query":
            esql_query = input("esql_query: ").strip()
            if not esql_query:
                print("Error: esql_query is required.")
                continue
            result = test_query(es_url, username, password, esql_query)
            print(result["message"] if result["success"] else f"Error: {result['message']}")
            continue

        if command == "run_query":
            esql_query = input("esql_query: ").strip()
            if not esql_query:
                print("Error: esql_query is required.")
                continue
            result = run_query(es_url, username, password, esql_query)
            print(result["message"] if result["success"] else f"Error: {result['message']}")
            continue

        if command == "ingest_doc":
            index_name = input("index_name: ").strip()
            mapping_file = input("mapping_file (path): ").strip()
            data_file = input("data_file (path): ").strip()

            if not index_name or not mapping_file or not data_file:
                print("Error: index_name, mapping_file, and data_file are required.")
                continue

            result = ingest_doc(es_url, username, password, index_name, mapping_file, data_file)
            print(result["message"] if result["success"] else f"Error: {result['message']}")
            continue

        if command == "delete_doc":
            index_name = input("index_name: ").strip()
            if not index_name:
                print("Error: index_name is required.")
                continue

            mode = input("mode (index|query): ").strip().lower()
            if mode not in {"index", "query"}:
                print("Error: mode must be 'index' or 'query'.")
                continue

            if mode == "index":
                result = delete_doc(es_url, username, password, index_name, query=None)
                print(result["message"] if result["success"] else f"Error: {result['message']}")
                continue

            query_str = input('query JSON (e.g., {"match_all":{}}): ').strip()
            if not query_str:
                print("Error: query JSON is required for mode=query.")
                continue

            try:
                query = json.loads(query_str)
            except json.JSONDecodeError as exc:
                print(f"Error: invalid JSON query: {exc}")
                continue

            result = delete_doc(es_url, username, password, index_name, query=query)
            print(result["message"] if result["success"] else f"Error: {result['message']}")
            continue

        print(f"Error: Unknown command '{command}'. Type 'help' for a list of available commands.")


if __name__ == "__main__":
    main()
