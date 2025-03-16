import json
import unittest

from starlette.testclient import TestClient

from andelsbolig.user.repository import UserRepository
from tests.generator import generate_user_create, generate_stripe_signed_payload
from .context import *
from .data.stripe.checkout_session_completed import generate_stripe_checkout_session_completed

user_db = UserRepository()


class TestPayment(unittest.TestCase):
    """
    # TODO: Tests på
    checkout.session.completed
    customer.subscription.updated
    customer.subscription.created
    """

    def test_new_user_and_subscription(self):
        """
        Test the following flow:
        1 Unauthenticated user can not use endpoints protected by is-authenticated
        2 Create a new user
        3 Authenticated but not subscribed user can not use endpoints protected by is-subscribed
        4 Create a new subscription
        5 Subscribed user can now use said endpoint
        """
        user_email = "newuser@example.com"
        # 1
        user_client = TestClient(andelsbolig.app)
        r1 = user_client.get("/is-authenticated")
        self.assertEqual(401, r1.status_code)

        # 2
        user_create = generate_user_create(user_email)
        r2 = user_client.post("/user", json=user_create.model_dump())
        self.assertEqual(200, r2.status_code)
        jwt = r2.json()["jwt"]
        user_client.headers = {"Authorization": f"Bearer {jwt}"}

        # 3
        r3 = user_client.get("/is-subscribed")
        self.assertEqual(403, r3.status_code)

        # 4
        # Payment is handled directly via GUI and Stripe, and thus we mock the "checkout.session.completed" which Stripe sends directly to us in dev/prod
        user_id = user_db.read({"email": user_email}).id
        mock = generate_stripe_checkout_session_completed(user_id)
        headers = {"stripe-signature": generate_stripe_signed_payload(json.dumps(mock))}
        r4 = user_client.post("/webhook", json=mock, headers=headers)
        self.assertEqual(200, r4.status_code)
        # Confirm user has subscribed
        user = user_db.read({"email": user_email})
        self.assertTrue(user.is_subscribed())

        # 5
        # Expect 404 since no advertisement exists but the user is authorized
        r5 = user_client.get("/is-subscribed")
        self.assertEqual(200, r5.status_code)
