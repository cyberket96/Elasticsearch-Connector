from __future__ import annotations

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ConnectionError,
    NotFoundError,
    TransportError,
)


def fetch_schema(es_url: str, username: str, password: str, index_name: str | None = None) -> dict:
    """
    Core Feature: Fetch Schema (Index Mappings)

    Fetches mappings using the Elasticsearch get mapping API.

    Standard response:
        {
          "success": bool,
          "message": str,
          "data": Any | None,
          "error": dict | None
        }

    Data returned:
    - Full mapping response as returned by `client.indices.get_mapping(...)`
      (dict keyed by index name)
    """
    try:
        client = Elasticsearch(
            [es_url],
            http_auth=(username, password),
            verify_certs=False,  # lab/dev convenience; enable CA verification in production
        )

        schema = client.indices.get_mapping(index=index_name) if index_name else client.indices.get_mapping()

        return {
            "success": True,
            "message": "Schema retrieved successfully.",
            "data": schema,
            "error": None,
        }

    except NotFoundError as e:
        # Typically happens if user passes an index/pattern that doesn't exist.
        return {
            "success": False,
            "message": "Index not found while fetching schema.",
            "data": {"index_name": index_name},
            "error": {"type": "NotFoundError", "details": str(e)},
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
            "message": "Elasticsearch transport error while fetching schema.",
            "data": None,
            "error": {"type": "TransportError", "details": str(e)},
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Unexpected error while fetching schema.",
            "data": None,
            "error": {"type": e.__class__.__name__, "details": str(e)},
        }
