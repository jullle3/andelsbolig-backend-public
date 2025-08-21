import hashlib
import hmac
import json
import time
import unittest

from starlette.testclient import TestClient

from andelsbolig.config.properties import RUNNING_TESTS, STRIPE_ENDPOINT_SECRET
from andelsbolig.security.service import create_jwt
from andelsbolig.user.repository import UserRepository
from tests.generator import generate_user_create
from .context import *
from tests import client


db = UserRepository()


class TestUser(unittest.TestCase):
    """ """

    # def test_user_created_in_stripe(self):
    #     """
    #     Test that a user is created in Stripe when a user is created in our app
    #     """
    #     user_create = generate_user_create("random@example.com")
    #     r1 = client.post("/user", json=user_create.model_dump())
    #
    #     user = db.read({"email": user_create.email})
    #     self.assertIsNotNone(user.stripe_id)
    #     db.delete({"email": user_create.email})
