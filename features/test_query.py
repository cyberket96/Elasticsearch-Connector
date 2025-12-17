# Feature : Test Query

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, AuthenticationException, AuthorizationException, TransportError

def test_query(es_url: str, username: str, password: str, esql_query: str):

    try:
        client = Elasticsearch(
            [es_url],
            http_auth=(username, password),
            verify_certs=False
        )

        response = client.esql.query(query=esql_query)

        print("Query tested successfully!")
        return {"success": True, "message": "Query tested successfully!", "response": response}

    except AuthenticationException:
        return {"success": False, "message": "Authentication failed. Please check your username and password."}
    except AuthorizationException:
        return {"success": False, "message": "Authorization failed. You do not have the required permissions."}
    except ConnectionError:
        return {"success": False, "message": "Failed to connect to Elasticsearch. Please check the URL and network."}
    except TransportError as e:
        return {"success": False, "message": f"Query execution failed: {e.info.get('error', {}).get('reason', 'Unknown error')}"}
    except Exception as e:
        return {"success": False, "message": f"An unexpected error occurred: {e}"}
