from __future__ import annotations

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import AuthenticationException, AuthorizationException, ConnectionError, TransportError


def fetch_indices(es_url: str, username: str, password: str) -> dict:
    """
    Core Feature: Fetch Indices

    Returns index inventory from Elasticsearch using the cat indices API.

    Standard response:
        {
          "success": bool,
          "message": str,
          "data": Any | None,
          "error": dict | None
        }

    Data returned:
    - List[dict] as returned by `client.cat.indices(format="json")`
    """
    try:
        client = Elasticsearch(
            [es_url],
            http_auth=(username, password),
            verify_certs=False,  # lab/dev convenience; enable CA verification in production
        )

        indices = client.cat.indices(format="json") or []

        return {
            "success": True,
            "message": "Indices retrieved successfully." if indices else "No indices found.",
            "data": indices,
            "error": None,
        }

    except AuthenticationException as e:
        return {
            "success": False,
            "message": "Authentication failed.",
            "data": None,
            "error": {"type": "AuthenticationException", "details": str(e)},
        }

    except AuthorizationException as e:
        return {
            "success": False,
            "message": "Authorization failed.",
            "data": None,
            "error": {"type": "AuthorizationException", "details": str(e)},
        }

    except ConnectionError as e:
        return {
            "success": False,
            "message": "Connection error.",
            "data": None,
            "error": {"type": "ConnectionError", "details": str(e)},
        }

    except TransportError as e:
        return {
            "success": False,
            "message": "Elasticsearch transport error while fetching indices.",
            "data": None,
            "error": {"type": "TransportError", "details": str(e)},
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Unexpected error while fetching indices.",
            "data": None,
            "error": {"type": e.__class__.__name__, "details": str(e)},
        }
