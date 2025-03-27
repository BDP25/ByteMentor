from pymongo import MongoClient
from pymongo.database import Database
from logger import LOGGER


def get_db() -> Database:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["bytementor"]
    return db


def load_to_mongodb(data: dict, collection_name: str = "text_extracted") -> None:
    try:
        db = get_db()
        collection = db[collection_name]
        collection.insert_one(data)
        LOGGER.info(f"Loading {data['filename']} to collection {collection_name}")
    except Exception as e:
        LOGGER.error(f"Failed to load {data['filename']}: {e}")


def extract_from_mongod(
    query: dict | None = None, collection_name: str = "text_extracted"
) -> list[dict] | None:
    try:
        db = get_db()
        collection = db[collection_name]
        if query and len(query) == 1:
            result = collection.find_one(query)
            return result
        if query:
            return list(collection.find(query))
        return list(collection.find({}))
    except Exception:
        LOGGER.error(f"Failed to extract from collection {collection_name}.")
        return None
