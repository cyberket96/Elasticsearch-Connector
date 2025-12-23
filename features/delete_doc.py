# Feature : Delete Documents

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, AuthenticationException, AuthorizationException

def delete_doc(es_url: str, username: str, password: str, index_name: str, query: dict = None):

    try:
        client = Elasticsearch(
            [es_url],
            http_auth=(username, password),
            verify_certs=False
        )

        if query:
            response = client.delete_by_query(index=index_name, body={"query": query})
            deleted_count = response["deleted"]
            print(f"{deleted_count} documents deleted successfully from index '{index_name}'.")
            return {"success": True, "message": f"{deleted_count} documents deleted successfully from index '{index_name}'."}
        else:
            client.indices.delete(index=index_name)
            print(f"Index '{index_name}' deleted successfully.")
            return {"success": True, "message": f"Index '{index_name}' deleted successfully."}

    except AuthenticationException:
        return {"success": False, "message": "Authentication failed. Please check your username and password."}
    except AuthorizationException:
        return {"success": False, "message": "Authorization failed. You do not have the required permissions."}
    except ConnectionError:
        return {"success": False, "message": "Failed to connect to Elasticsearch. Please check the URL and network."}
    except Exception as e:
        return {"success": False, "message": f"An unexpected error occurred: {e}"}
