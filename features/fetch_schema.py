# Feature : Fetch Schema

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, AuthenticationException, AuthorizationException

def fetch_schema(es_url: str, username: str, password: str, index_name: str = None):

    try:
        client = Elasticsearch(
            [es_url],
            http_auth=(username, password),
            verify_certs=False
        )

        if index_name:
            schema = client.indices.get_mapping(index=index_name)
        else:
            schema = client.indices.get_mapping()

        print("Index Schema:")
        for index, mappings in schema.items():
            print(f"\nIndex: {index}")
            print(f"{'Field Name':<30} {'Data Type':<15}")
            print("-" * 50)
            properties = mappings["mappings"].get("properties", {})
            for field, details in properties.items():
                data_type = details.get("type", "object")
                print(f"{field:<30} {data_type:<15}")

        return {"success": True, "message": "Schema retrieved successfully.", "schema": schema}

    except AuthenticationException:
        return {"success": False, "message": "Authentication failed. Please check your username and password."}
    except AuthorizationException:
        return {"success": False, "message": "Authorization failed. You do not have the required permissions."}
    except ConnectionError:
        return {"success": False, "message": "Failed to connect to Elasticsearch. Please check the URL and network."}
    except Exception as e:
        return {"success": False, "message": f"An unexpected error occurred: {e}"}
