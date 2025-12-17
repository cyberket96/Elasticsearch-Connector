# Feature : Fetch Indices

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, AuthenticationException, AuthorizationException

def fetch_indices(es_url: str, username: str, password: str):

    try:
        client = Elasticsearch(
            [es_url],
            http_auth=(username, password),
            verify_certs=False 
        )

        indices = client.cat.indices(format="json")

        if not indices:
            print("No indices found in the Elasticsearch cluster.")
            return {"success": True, "message": "No indices found in the Elasticsearch cluster.", "indices": []}

        print(f"{'Index Name':<30} {'Health':<10} {'Status':<10} {'Docs Count':<15} {'Store Size':<15}")
        print("-" * 80)
        for index in indices:
            print(f"{index['index']:<30} {index['health']:<10} {index['status']:<10} {index['docs.count']:<15} {index['store.size']:<15}")

        return {"success": True, "message": "Indices retrieved successfully.", "indices": indices}

    except AuthenticationException:
        return {"success": False, "message": "Authentication failed. Please check your username and password."}
    except AuthorizationException:
        return {"success": False, "message": "Authorization failed. You do not have the required permissions."}
    except ConnectionError:
        return {"success": False, "message": "Failed to connect to Elasticsearch. Please check the URL and network."}
    except Exception as e:
        return {"success": False, "message": f"An unexpected error occurred: {e}"}
