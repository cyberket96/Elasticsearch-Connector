# Feature: Featch Health

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, AuthenticationException, AuthorizationException

def get_cluster_health(es_url: str, username: str, password: str):
  
    try:
        client = Elasticsearch(
            [es_url],
            http_auth=(username, password),
            verify_certs=False
        )

        health = client.cluster.health()

        print("Cluster Health Information:")
        print(f"Status: {health['status']}")
        print(f"Number of Nodes: {health['number_of_nodes']}")
        print(f"Number of Data Nodes: {health['number_of_data_nodes']}")
        print(f"Active Shards: {health['active_shards']}")
        print(f"Initializing Shards: {health['initializing_shards']}")
        print(f"Unassigned Shards: {health['unassigned_shards']}")

        return {"success": True, "message": "Cluster health retrieved successfully!", "health": health}

    except AuthenticationException:
        return {"success": False, "message": "Authentication failed. Please check your username and password."}
    except AuthorizationException:
        return {"success": False, "message": "Authorization failed. You do not have the required permissions."}
    except ConnectionError:
        return {"success": False, "message": "Failed to connect to Elasticsearch. Please check the URL and network."}
    except Exception as e:
        return {"success": False, "message": f"An unexpected error occurred: {e}"}
  
