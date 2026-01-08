# Feature : test Connection

from __future__ import annotations

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import AuthenticationException, AuthorizationException, ConnectionError


def test_connection(es_url: str, username: str, password: str) -> dict:

    try:
        client = Elasticsearch(
            [es_url],
            http_auth=(username, password),
            verify_certs=False,
        )

        ok = client.ping()
        if ok:
            return {
                "success": True,
                "message": "Connection successful.",
                "data": {"reachable": True},
                "error": None,
            }

        return {
            "success": False,
            "message": "Connection failed (ping returned false).",
            "data": {"reachable": False},
            "error": {
                "type": "PingFailed",
                "details": "Elasticsearch ping returned false without an exception.",
            },
        }

    except AuthenticationException as e:
        return {
            "success": False,
            "message": "Authentication failed.",
            "data": {"reachable": False},
            "error": {"type": "AuthenticationException", "details": str(e)},
        }

    except AuthorizationException as e:
        return {
            "success": False,
            "message": "Authorization failed.",
            "data": {"reachable": False},
            "error": {"type": "AuthorizationException", "details": str(e)},
        }

    except ConnectionError as e:
        return {
            "success": False,
            "message": "Connection error.",
            "data": {"reachable": False},
            "error": {"type": "ConnectionError", "details": str(e)},
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Unexpected error while testing connection.",
            "data": {"reachable": False},
            "error": {"type": e.__class__.__name__, "details": str(e)},
        }
