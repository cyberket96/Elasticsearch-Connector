# Feature: Test Connection

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, AuthenticationException, AuthorizationException

def test_connection(es_url: str, username: str, password: str):
    try:
        client = Elasticsearch([es_url], http_auth=(username, password), verify_certs=False)

        if client.cluster.health():
            print("Connection successful!")
        else:
            print("Connection failed!")
    except AuthenticationException:
        print("Authentication failed. Please check your username and password.")
    except AuthorizationException:
        print("Authorization failed. You do not have the required permissions.")
    except ConnectionError:
        print("Failed to connect to Elasticsearch. Please check the URL and network.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
