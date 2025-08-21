import unittest

from andelsbolig.advertisement.repository import AdvertisementRepository
from andelsbolig.config.properties import RUNNING_TESTS
from andelsbolig.comment_thread.repository import ThreadRepository
from definitions import ROOT_DIR
from tests import client, test_suite_user_id
from tests.generator import generate_advertisement_create, generate_comment_create

db = ThreadRepository()


class TestAdvertisement(unittest.TestCase):

    @classmethod
    def tearDown(cls) -> None:
        if RUNNING_TESTS:
            db.delete_collection()

    def test_create_comment(self):
        """
        Test creating comments for an advertisement and retrieving the thread.

        Steps:
        1. Create an advertisement.
        2. Post two comments to the advertisement.
        3. Retrieve the thread and verify the number of comments.
        """
        advertisement_create = generate_advertisement_create()
        r1 = client.post("/advertisement", json=advertisement_create)
        advertisement_id = r1.json()

        r2 = client.post(
            "/comment", json=generate_comment_create("fuck en grim lejlighed", advertisement_id).model_dump()
        )
        r3 = client.post(
            "/comment", json=generate_comment_create("Det kan du selv være, din fede ko", advertisement_id).model_dump()
        )

        r4 = client.get(f"/thread/{advertisement_id}")
        self.assertEqual(2, len(r4.json()["comments"]))
