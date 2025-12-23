# Feature : Ingest Documents

import json
import random
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import ConnectionError, AuthenticationException, AuthorizationException

def ingest_doc(es_url: str, username: str, password: str, index_name: str, mapping_file: str, data_file: str):

    try:
        client = Elasticsearch(
            [es_url],
            http_auth=(username, password),
            verify_certs=False
        )

        if client.indices.exists(index=index_name):
            print(f"Index '{index_name}' already exists. Skipping index creation.")
        else:
            with open(mapping_file, "r") as file:
                mapping = json.load(file)

            client.indices.create(index=index_name, body=mapping)
            print(f"Index '{index_name}' created successfully.")

        with open(data_file, "r") as file:
            documents = json.load(file)

        now = datetime.utcnow()
        fifteen_minutes_ago = now - timedelta(minutes=15)
        for doc in documents:
            random_timestamp = fifteen_minutes_ago + timedelta(
                seconds=random.randint(0, 15 * 60)
            )
            doc["@timestamp"] = random_timestamp.isoformat()

        actions = [
            {
                "_index": index_name,
                "_source": doc
            }
            for doc in documents
        ]

        success, _ = bulk(client, actions)
        print(f"{success} documents ingested successfully into index '{index_name}'.")

        return {"success": True, "message": f"{success} documents ingested successfully into index '{index_name}'."}

    except AuthenticationException:
        return {"success": False, "message": "Authentication failed. Please check your username and password."}
    except AuthorizationException:
        return {"success": False, "message": "Authorization failed. You do not have the required permissions."}
    except ConnectionError:
        return {"success": False, "message": "Failed to connect to Elasticsearch. Please check the URL and network."}
    except Exception as e:
        return {"success": False, "message": f"An unexpected error occurred: {e}"}
