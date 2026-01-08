# Feature : Ingest Doc

from __future__ import annotations

import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ConnectionError,
    RequestError,
    TransportError,
)
from elasticsearch.helpers import bulk


def ingest_doc(
    es_url: str,
    username: str,
    password: str,
    index_name: str,
    mapping_file: str,
    data_file: str,
) -> dict:

    try:
        client = Elasticsearch(
            [es_url],
            http_auth=(username, password),
            verify_certs=False,
        )

        mapping_path = Path(mapping_file)
        data_path = Path(data_file)

        if not mapping_path.is_file():
            return {
                "success": False,
                "message": "Mapping file not found.",
                "data": {"mapping_file": mapping_file},
                "error": {"type": "FileNotFound", "details": f"Missing mapping file: {mapping_file}"},
            }

        if not data_path.is_file():
            return {
                "success": False,
                "message": "Data file not found.",
                "data": {"data_file": data_file},
                "error": {"type": "FileNotFound", "details": f"Missing data file: {data_file}"},
            }

        created_index = False
        if not client.indices.exists(index=index_name):
            with mapping_path.open("r", encoding="utf-8") as f:
                mapping = json.load(f)

            client.indices.create(index=index_name, body=mapping)
            created_index = True

        with data_path.open("r", encoding="utf-8") as f:
            documents = json.load(f)

        if isinstance(documents, dict):
            documents = [documents]

        if not isinstance(documents, list):
            return {
                "success": False,
                "message": "Invalid data file format. Expected a JSON array (list) or a single JSON object.",
                "data": {"data_file": data_file},
                "error": {
                    "type": "InvalidInput",
                    "details": "Data JSON must be a list of documents or a single document object.",
                },
            }

        for doc in documents:
            if not isinstance(doc, dict):
                return {
                    "success": False,
                    "message": "Invalid document format in data file. Each item must be a JSON object.",
                    "data": {"data_file": data_file},
                    "error": {"type": "InvalidInput", "details": "Each document must be a JSON object (dict)."},
                }

        now = datetime.now(timezone.utc)
        start = now - timedelta(minutes=15)

        for doc in documents:
            random_ts = start + timedelta(seconds=random.randint(0, 15 * 60))
            doc["@timestamp"] = random_ts.isoformat()

        actions = ({"_index": index_name, "_source": doc} for doc in documents)
        ingested_count, errors = bulk(client, actions, raise_on_error=False)

        if errors:
            return {
                "success": False,
                "message": "Bulk ingest completed with errors.",
                "data": {
                    "index": index_name,
                    "created_index": created_index,
                    "requested_docs": len(documents),
                    "ingested_docs": ingested_count,
                    "bulk_errors": errors,
                },
                "error": {"type": "BulkIngestError", "details": "One or more bulk items failed."},
            }

        return {
            "success": True,
            "message": "Documents ingested successfully.",
            "data": {
                "index": index_name,
                "created_index": created_index,
                "requested_docs": len(documents),
                "ingested_docs": ingested_count,
                "timestamp_window_minutes": 15,
                "timestamp_field": "@timestamp",
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

    except RequestError as e:
        return {
            "success": False,
            "message": "Elasticsearch request error during ingest.",
            "data": None,
            "error": {"type": "RequestError", "details": str(e)},
        }

    except TransportError as e:
        return {
            "success": False,
            "message": "Elasticsearch transport error during ingest.",
            "data": None,
            "error": {"type": "TransportError", "details": str(e)},
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Unexpected error during ingest.",
            "data": None,
            "error": {"type": e.__class__.__name__, "details": str(e)},
        }
