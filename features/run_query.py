from __future__ import annotations

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ConnectionError,
    TransportError,
)


def run_query(es_url: str, username: str, password: str, esql_query: str) -> dict:
    """
    Core Feature: Run ES|QL Query

    Executes an ES|QL query and returns results (no printing).

    Standard response:
        {
          "success": bool,
          "message": str,
          "data": Any | None,
          "error": dict | None
        }

    Data returned (on success):
        {
          "columns": [{"name": "...", "type": "..."} ...],
          "values":  [[...], [...]],
          "took": int | None,
          "is_partial": bool | None
        }
    """
    try:
        if not esql_query or not esql_query.strip():
            return {
                "success": False,
                "message": "ES|QL query is required.",
                "data": None,
                "error": {"type": "InvalidInput", "details": "esql_query was empty."},
            }

        client = Elasticsearch(
            [es_url],
            http_auth=(username, password),
            verify_certs=False,  # lab/dev convenience; enable CA verification in production
        )

        response = client.esql.query(query=esql_query)

        # ES|QL responses typically contain: columns, values, took, is_partial
        columns = response.get("columns", [])
        values = response.get("values", [])

        return {
            "success": True,
            "message": "Query executed successfully.",
            "data": {
                "columns": columns,
                "values": values,
                "took": response.get("took"),
                "is_partial": response.get("is_partial"),
            },
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
        # Try to extract ES error details when present
        reason = None
        try:
            reason = (e.info or {}).get("error", {}).get("reason")
        except Exception:
            reason = None

        return {
            "success": False,
            "message": "ES|QL query execution failed.",
            "data": None,
            "error": {
                "type": "TransportError",
                "details": reason or str(e),
            },
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Unexpected error while executing ES|QL query.",
            "data": None,
            "error": {"type": e.__class__.__name__, "details": str(e)},
        }
