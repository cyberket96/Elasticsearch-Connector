# Feature : Delete Doc

from __future__ import annotations

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ConnectionError,
    NotFoundError,
    TransportError,
)


def delete_doc(es_url: str, username: str, password: str, index_name: str, query: dict | None = None) -> dict:

    try:
        client = Elasticsearch(
            [es_url],
            http_auth=(username, password),
            verify_certs=False,
        )

        if query is not None:

            resp = client.delete_by_query(index=index_name, body={"query": query})

            deleted = resp.get("deleted", 0)
            took = resp.get("took")
            timed_out = resp.get("timed_out", False)
            failures = resp.get("failures", [])

            if failures and deleted == 0:
                return {
                    "success": False,
                    "message": f"Delete-by-query completed with failures for index '{index_name}'.",
                    "data": {
                        "index": index_name,
                        "mode": "delete_by_query",
                        "deleted": deleted,
                        "took_ms": took,
                        "timed_out": timed_out,
                        "failures": failures,
                    },
                    "error": {"type": "DeleteByQueryFailed", "details": "Elasticsearch returned failures."},
                }

            return {
                "success": True,
                "message": f"Delete-by-query completed for index '{index_name}'.",
                "data": {
                    "index": index_name,
                    "mode": "delete_by_query",
                    "deleted": deleted,
                    "took_ms": took,
                    "timed_out": timed_out,
                    "failures": failures,
                },
                "error": None,
            }

        resp = client.indices.delete(index=index_name)

        return {
            "success": True,
            "message": f"Index '{index_name}' deleted.",
            "data": {
                "index": index_name,
                "mode": "delete_index",
                "acknowledged": resp.get("acknowledged"),
            },
            "error": None,
        }

    except NotFoundError as e:

        return {
            "success": False,
            "message": f"Index '{index_name}' not found.",
            "data": {"index": index_name, "mode": "delete_index" if query is None else "delete_by_query"},
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
            "message": "Elasticsearch transport error during delete operation.",
            "data": None,
            "error": {"type": "TransportError", "details": str(e)},
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Unexpected error during delete operation.",
            "data": None,
            "error": {"type": e.__class__.__name__, "details": str(e)},
        }
