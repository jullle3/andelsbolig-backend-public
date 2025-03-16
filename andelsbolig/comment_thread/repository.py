from pymongo import IndexModel

from andelsbolig.misc.mongo import MongoStorage
from andelsbolig.comment_thread.model import CommentThread


class ThreadRepository(MongoStorage):
    def __init__(self):
        super().__init__("andelsbolig_basen", "thread")

        indexes = [
            IndexModel("referenced_id"),
        ]
        self.col.create_indexes(indexes)

    def create(self, thread: CommentThread):
        return self.col.insert_one(thread.model_dump(by_alias=True))

    def read(self, filter_: dict) -> CommentThread:
        doc = self.col.find_one(filter_)
        return CommentThread(**doc) if doc else None
