# Main 

import os
import argparse
from dotenv import load_dotenv
from features.test_connection import test_connection
from features.list_indices import list_indices
from features.test_query import test_query
from features.adhoc_query import adhoc_query

def main():

    load_dotenv()

    # Fetch Elasticsearch credentials from environment variables
    es_url = os.getenv("ES_URL")
    username = os.getenv("ES_USERNAME")
    password = os.getenv("ES_PASSWORD")

    # Validate that all required credentials are provided
    if not es_url or not username or not password:
        print("Error: Missing Elasticsearch credentials in the .env file.")
        return

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Elastic Connector: A command-line tool for Elasticsearch operations.")
    parser.add_argument(
        "feature",
        choices=["test_connection", "list_indices", "test_query", "adhoc_query"],
        help="The feature to execute. Options: test_connection, list_indices, test_query, adhoc_query"
    )
    parser.add_argument(
        "--esql_query",
        help="The ES|QL query to test (required for the 'test_esql' feature)."
    )
    args = parser.parse_args()

    # Execute the selected feature
    if args.feature == "test_connection":
        result = test_connection(es_url, username, password)
    elif args.feature == "list_indices":
        result = list_indices(es_url, username, password)
    elif args.feature == "test_query":
        if not args.esql_query:
            print("Error: --esql_query is required for the 'test_esql' feature.")
            return
        result = test_query(es_url, username, password, args.esql_query)
    elif args.feature == "adhoc_query":
        if not args.esql_query:
            print("Error: --esql_query is required for the 'adhoc_query' feature.")
            return
        result = adhoc_query(es_url, username, password, args.esql_query)

    # Print the result
    if result["success"]:
        print(result["message"])
    else:
        print(f"Error: {result['message']}")

if __name__ == "__main__":
    main()
