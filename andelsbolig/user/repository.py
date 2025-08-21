from pymongo import IndexModel

from andelsbolig.misc.mongo import MongoStorage
from andelsbolig.user.model import User


class UserRepository(MongoStorage):
    """ """

    def __init__(self):
        super().__init__("andelsbolig_basen", "user")

        # Indexes er som default ASCENDING
        indexes = [
            IndexModel("email"),
        ]
        self.col.create_indexes(indexes)

    def create(self, user: User):
        return self.col.insert_one(user.model_dump(by_alias=True))

    def read(self, filter_: dict) -> User:
        doc = self.col.find_one(filter_)
        return User.model_construct(**doc) if doc else None
