import unittest

from andelsbolig.advertisement.repository import AdvertisementRepository
from andelsbolig.config.properties import RUNNING_TESTS
from definitions import ROOT_DIR
from tests import client, test_suite_user_id, client2
from tests.generator import generate_advertisement_create

db = AdvertisementRepository()


class TestAdvertisement(unittest.TestCase):

    @classmethod
    def tearDown(cls) -> None:
        if RUNNING_TESTS:
            db.delete_collection()

    def test_partial_updates_to_advertisement(self):
        """Upload of file by user should associate given file to the users advertisement, even when advertisement doesn't exist yet"""
        with open(f"{ROOT_DIR}/tests/data/car.png", "rb") as file:
            files = {"file": ("car.png", file, "image/png")}
            r1 = client.post("/upload", files=files)

        advertisement = db.read({})

        self.assertIn("url", advertisement.images[0])
        self.assertIn("thumbnail_url", advertisement.images[0])

        # User eventually submits the full form
        advertisement_create = generate_advertisement_create()
        r2 = client.post("/advertisement", json=advertisement_create)
        self.assertEqual(200, r1.status_code)

        # Ensure only one advertisement is created
        self.assertTrue(db.exists({"created_by": test_suite_user_id}, 1))

        # Ensure fields are updated correctly
        updated_advertisement = db.read({})
        self.assertIn("url", updated_advertisement.images[0])
        self.assertIn("thumbnail_url", updated_advertisement.images[0])

        r3 = client.delete(f"/upload/thumbnail_car.png")
        # 200 means image was deleted
        self.assertEqual(200, r3.status_code)

    def test_crud(self):
        # Create
        advertisement = generate_advertisement_create()
        r1 = client.post("/advertisement", json=advertisement)
        self.assertEqual(200, r1.status_code)
        advertisement_id = r1.json()

        # Read
        r2 = client.get(f"/advertisement/{advertisement_id}")
        self.assertEqual(200, r2.status_code)

        # Delete (not supported yet)
        # r3 = client.delete("/advertisement", params={"_id": advertisement_id})
        # self.assertTrue(db.exists({"_id": advertisement_id, "deleted": True}, 1))

    def test_queries(self):
        # Opret 2 forskellige
        advertisement = generate_advertisement_create()
        advertisement["city"] = "Odense"
        r1 = client.post("/advertisement", json=advertisement)
        advertisement2 = generate_advertisement_create()
        advertisement2["city"] = "København"
        r2 = client.post("/advertisement", json=advertisement2)

        # Read
        r3 = client.get("/advertisement", params={"text": "København"})
        self.assertEqual(1, r3.json()["total_object_count"])

    def test_radius_search(self):
        # Create 2 advertisements, query by radius and expect only 1 match
        advertisement = generate_advertisement_create()
        advertisement["location"] = {"type": "Point", "coordinates": [12.5684, 55.6762]}  # Copenhagen
        advertisement["city"] = "København"
        advertisement["postal_number"] = "1051"
        r1 = client.post("/advertisement", json=advertisement)
        advertisement2 = generate_advertisement_create()
        advertisement2["location"] = {"type": "Point", "coordinates": [10.4024, 55.4038]}  # Odense
        advertisement2["city"] = "Odense"
        advertisement2["postal_number"] = 5200
        r2 = client2.post("/advertisement", json=advertisement2)

        # Query for advertisements within 20 km of Copenhagen
        r3 = client.get("/advertisement", params={"radius": 20, "postal_number": 1051})
        matched_advertisement = r3.json()["objects"][0]
        self.assertEqual("København", matched_advertisement["city"])

    def test_favorite(self):
        # Favorite 2 advertisements, remove 1 favorite, ensure query by favorites only returns 1
        advertisement = generate_advertisement_create()
        r1 = client.post("/advertisement", json=advertisement)
        advertisement_id = r1.json()
        advertisement2 = generate_advertisement_create()
        r2 = client2.post("/advertisement", json=advertisement2)
        advertisement_id2 = r2.json()

        user_patch_payload = {"favorite_advertisement_add_operation": True, "favorite_advertisement": advertisement_id}
        user_patch_payload2 = {
            "favorite_advertisement_add_operation": True,
            "favorite_advertisement": advertisement_id2,
        }

        # Send the request to update the user document
        r3 = client.patch("/user", json=user_patch_payload)
        r4 = client.patch("/user", json=user_patch_payload2)

        # Ensure both favorites are stored
        r5 = client.get(f"/user/{test_suite_user_id}")
        user = r5.json()
        self.assertEqual(2, len(user["favorite_advertisements"]))

        # Delete 1 entry
        user_patch_payload = {"favorite_advertisement_add_operation": False, "favorite_advertisement": advertisement_id}
        r6 = client.patch("/user", json=user_patch_payload)

        r7 = client.get(f"/user/{test_suite_user_id}")
        user_after_delete = r7.json()
        self.assertEqual(1, len(user_after_delete["favorite_advertisements"]))

        r8 = client.get(f"/advertisement", params={'favorites_only': True})
        favorited_advertisement = r8.json()["objects"][0]
        self.assertEqual(advertisement_id2, favorited_advertisement["_id"])

    def test_sort(self):
        r1 = client.get("/advertisement", params={"sort": "created-asc"})
        r2 = client.get("/advertisement", params={"sort": "created-desc"})