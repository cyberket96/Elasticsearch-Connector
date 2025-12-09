# Main 

import os
import argparse
from dotenv import load_dotenv
from features.test_connection import test_connection

def main():

    load_dotenv()
    es_url = os.getenv("ES_URL")
    username = os.getenv("ES_USERNAME")
    password = os.getenv("ES_PASSWORD")

    if not es_url or not username or not password:
        print("Error: Missing Elasticsearch credentials in the .env file.")
        return

    parser = argparse.ArgumentParser(description="Elastic Connector: A command-line tool for Elasticsearch operations.")
    parser.add_argument(
        "feature",
        choices=["test_connection"],
        help="The feature to execute. Options: test_connection"
    )

    args = parser.parse_args()

    if args.feature == "test_connection":
        result = test_connection(es_url, username, password)

    if result["success"]:
        print(result["message"])
    else:
        print(f"Error: {result['message']}")

if __name__ == "__main__":
    main()
