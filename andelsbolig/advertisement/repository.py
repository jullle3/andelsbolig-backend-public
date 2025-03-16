import pymongo
from pymongo import IndexModel, ReturnDocument

from andelsbolig.advertisement.model import Advertisement
from andelsbolig.misc.mongo import MongoStorage


class AdvertisementRepository(MongoStorage):
    def __init__(self):
        super().__init__("andelsbolig_basen", "advertisement")

        # Indexes er som default ASCENDING
        indexes = [
            IndexModel(
                [
                    ("title", "text"),
                    ("description", "text"),
                    ("city", "text"),
                    ("postal_number", "text"),
                    ("address", "text"),
                ],
            ),
            IndexModel("created_by"),
            IndexModel("postal_number"),
            IndexModel([("location", "2dsphere")]),
            IndexModel("created"),
            IndexModel("price"),
            IndexModel("monthly_fee"),
            IndexModel("square_meters"),
            # Åbenbart kun brugbart i Mongo Atlas
            # IndexModel(
            #     [("$**", "text")],  # Wildcard text index
            #     name="search_index",
            #     default_language="danish",
            #     weights={"title": 10, "description": 5, "city": 10, "postal_number": 10, "address": 5},
            # )
        ]
        self.col.create_indexes(indexes)

    def create(self, advertisement: Advertisement):
        return self.col.insert_one(advertisement.model_dump(by_alias=True))

    def read(self, filter_: dict) -> Advertisement:
        doc = self.col.find_one(filter_)
        return Advertisement.model_construct(**doc) if doc else None

    def read_and_update(self, filter_: dict, update: dict) -> Advertisement:
        doc = self.col.find_one_and_update(filter_, update, return_document=ReturnDocument.AFTER)
        return Advertisement.model_construct(**doc) if doc else None

    # noinspection PyMethodOverriding
    def replace(self, advertisement: Advertisement, upsert=False):
        filter_ = {"created_by": advertisement.created_by}
        doc = Advertisement.model_dump(advertisement, by_alias=True)
        if upsert:
            return self.col.replace_one(filter_, doc, upsert=True)
        else:
            return self.col.replace_one(filter_, doc)

    def read_paged(self, mongo_filter: dict, page: int, size: int, sort_field: str, direction: pymongo.ASCENDING | pymongo.DESCENDING) -> dict:
        """
        Perform paginated search.
        """
        if sort_field:
            cursor = self.col.find(mongo_filter).skip(page * size).limit(size).sort(sort_field, direction)
        else:
            cursor = self.col.find(mongo_filter).skip(page * size).limit(size)

        advertisements = [Advertisement.model_construct(**obj) for obj in list(cursor)]
        total_count = self.col.count_documents(mongo_filter)
        return {"objects": advertisements, "total_object_count": total_count, "count": len(advertisements)}
