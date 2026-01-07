from __future__ import annotations

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ConnectionError,
    TransportError,
)


def test_query(es_url: str, username: str, password: str, esql_query: str) -> dict:
    """
    Core Feature: Test ES|QL Query

    Purpose:
    - Validate that an ES|QL query can be executed successfully.
    - Does NOT format/print results (CLI/UI responsibility).

    Standard response:
        {
          "success": bool,
          "message": str,
          "data": Any | None,
          "error": dict | None
        }

    Data returned (on success):
    - A small execution summary (not full result set):
        {
          "took": int | None,
          "is_partial": bool | None,
          "columns_count": int,
          "rows_count": int
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

        resp = client.esql.query(query=esql_query)

        columns = resp.get("columns", []) or []
        values = resp.get("values", []) or []

        return {
            "success": True,
            "message": "Query tested successfully.",
            "data": {
                "took": resp.get("took"),
                "is_partial": resp.get("is_partial"),
                "columns_count": len(columns),
                "rows_count": len(values),
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
        reason = None
        try:
            reason = (e.info or {}).get("error", {}).get("reason")
        except Exception:
            reason = None

        return {
            "success": False,
            "message": "ES|QL query test failed.",
            "data": None,
            "error": {"type": "TransportError", "details": reason or str(e)},
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Unexpected error while testing ES|QL query.",
            "data": None,
            "error": {"type": e.__class__.__name__, "details": str(e)},
        }
