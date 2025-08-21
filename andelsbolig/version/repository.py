import datetime

from andelsbolig.misc.mongo import MongoStorage


class VersionRepository(MongoStorage):
    """
    Lagrer info om systemets nuværende version.
    """

    def __init__(self):
        super().__init__("andelsbolig_basen", "version")

        # Ensure document confirming application version always exists.
        # Note that the migration.service.py will handle migrations/upgrades from version 1.0 and upwards accordingly.
        if not self.exists({"_id": "version"}, 1):
            self.create({"_id": "version", "version": "1.0", "release_date": datetime.datetime.now()})

    def update_version(self, version: str) -> None:
        update = {"$set": {"version": version, "release_date": datetime.datetime.now()}}
        self.col.update_one({"_id": "version"}, update)
