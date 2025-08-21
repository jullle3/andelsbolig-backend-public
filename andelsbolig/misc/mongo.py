import os
from typing import List, Type, TypeVar

from pymongo import MongoClient
from pymongo.cursor import Cursor

from andelsbolig.misc.logger import get_logger
from pydantic import BaseModel, Field, EmailStr

logger = get_logger(__name__)
ModelType = TypeVar("ModelType", bound=BaseModel)


def create_mongo_client() -> MongoClient:
    """Create mongo client with sane defaults"""
    uri = os.environ.get("MONGO_URI", "localhost")

    logger.info(f"Connecting to MongoDB {uri=} ")
    # # Support both TLS and non TLS MongoClients
    # client = MongoClient(
    #     host=host,
    #     port=port,
    #     username=os.environ.get("MONGO_USERNAME", None),
    #     password=os.environ.get("MONGO_PASSWORD", None),
    # )
    # logger.info(f"Connected to MongoDB :)")
    client = MongoClient(uri)
    return client


class MongoStorage:
    """
    Base class for handling storage with MongoDB
    """

    _instances = []
    _client = create_mongo_client()

    def __init__(self, db: str, col: str):
        self._db = self._client[db]
        if col:
            self.col = self._db[col]
        self._instances.append(self)

    def get_db(self):
        """
        Will simply return the DB, for further usage.
        :return: db
        """
        return self._db

    def reload(self):
        """
        Primarily used for automated tests
        reloads the collection with the newest value
        """
        self.col = self._db[self.col.name]

    def create(self, obj: dict):
        return self.col.insert_one(obj)

    def create_many(self, objects: list):
        return self.col.insert_many(objects)

    def read(self, filter_: dict) -> dict:
        return self.col.find_one(filter_)

    def read_many(self, filter_: dict, cls: Type[ModelType]) -> list[ModelType]:
        cursor = self.col.find(filter_)
        return cursor_to_objects(cursor, cls)

    def replace(self, filter_: dict, obj: dict, upsert=False):
        if upsert:
            return self.col.replace_one(filter_, obj, upsert=True)
        else:
            return self.col.replace_one(filter_, obj)

    def update(self, filter_: dict, modifications: dict):
        return self.col.update_one(filter_, modifications)

    def update_many(self, filter_: dict, modifications: dict):
        return self.col.update_many(filter_, modifications)

    def delete(self, filter_: dict):
        self.col.delete_one(filter_)

    def delete_many(self, filter_: dict):
        self.col.delete_many(filter_)

    def delete_collection(self):
        return self.col.drop()

    def bulk_write(self, bulk: list):
        self.col.bulk_write(bulk)

    # def read_paged_aggregation(self, aggregation: list) -> dict:
    #     """ """
    #     results = self.col.aggregate(aggregation)
    #     return results
    #     return {"objects": objects, "total_object_count": count, "count": len(objects)}

    def exists(self, mongo_filter, count) -> bool:
        """
        Checks whether 'count' number of doc(s) exist for the given filter

        Args:
            mongo_filter:
            count: Antal dokumenter der forventes
        """
        return self.col.count_documents(mongo_filter) == count

    def healthcheck(self):
        """
        Ensure client can communicate with Mongo by calling server_info() to force an actual connection to mongo

        Will raise exception if connection fails
        """
        self._client.server_info()


def dict_to_object(doc: dict, cls: Type[ModelType]) -> list[ModelType]:
    return cls(**doc)


def cursor_to_objects(cursor: Cursor, cls: Type[ModelType]) -> list[ModelType]:
    """
    Convert a cursor to a list of specified class objects.

    Args:
        cursor (Cursor): The cursor to convert.
        cls (Type[BaseModel]): The class to convert the documents to.

    Returns:
        List[BaseModel]: The list of converted class objects.
    """
    return [dict_to_object(doc, cls) for doc in cursor]
