import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.collection import Collection

# Environment
DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "app_db")

_client: Optional[MongoClient] = None
_db = None


def get_db():
    global _client, _db
    if _db is None:
        _client = MongoClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db


def get_collection(name: str) -> Collection:
    db = get_db()
    return db[name]


def ensure_indexes():
    # Basic helpful indexes
    get_collection("post").create_index([("slug", ASCENDING)], unique=True)
    get_collection("project").create_index([("slug", ASCENDING)], unique=True)
    get_collection("post").create_index([("created_at", DESCENDING)])
    get_collection("project").create_index([("created_at", DESCENDING)])


def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    col = get_collection(collection_name)
    now = datetime.utcnow()
    payload = {**data, "created_at": now, "updated_at": now}
    result = col.insert_one(payload)
    doc = col.find_one({"_id": result.inserted_id})
    if doc:
        doc["_id"] = str(doc["_id"])  # serialize id
    return doc or {}


def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 10) -> List[Dict[str, Any]]:
    col = get_collection(collection_name)
    cursor = col.find(filter_dict or {}).sort("created_at", DESCENDING).limit(limit)
    docs = []
    for d in cursor:
        d["_id"] = str(d["_id"])  # serialize id
        docs.append(d)
    return docs


# Initialize indexes when module loads
try:
    ensure_indexes()
except Exception:
    # Index creation failure shouldn't crash app startup in ephemeral envs
    pass
