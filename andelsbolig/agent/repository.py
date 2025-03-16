from pymongo import IndexModel, ReturnDocument

from andelsbolig.advertisement.model import Advertisement
from andelsbolig.misc.mongo import MongoStorage


class AgentRepository(MongoStorage):
    def __init__(self):
        super().__init__("andelsbolig_basen", "agent")

        # Indexes er som default ASCENDING
        indexes = [
            IndexModel("created_by"),
        ]
        self.col.create_indexes(indexes)
