from andelsbolig.version import VERSION
from andelsbolig.version.migrations import migrations
from andelsbolig.version.repository import VersionRepository
from andelsbolig.misc.logger import get_logger

# db = VersionRepository()
# logger = get_logger(__name__)
#
#
# def check_for_upgrade():
#     """Opdaterer systemets version og - om nødvendigt - udfører en migrering"""
#     doc = db.read({"_id": "version"})
#
#     if doc["version"] != VERSION:
#         logger.info("New version!")
#         # Do we have to migrate?
#         if VERSION in migrations:
#             logger.info("Starting migration...")
#
#             # Execute the actual migration
#             migrations[VERSION]()
#
#             logger.info("Migration successfully completed")
#
#         # Update version
#         db.update_version(VERSION)
#         logger.info(f"Updated application version from {doc['version']} -> {VERSION}")
#
#     logger.info("Application up to date :)")
