import os

# Setup test environment
os.environ["RUNNING_TESTS"] = "TRUE"

from .generator import generate_user_create, generate_stripe_signed_payload, generate_subscribed_client
from .context import *
from andelsbolig.user.repository import UserRepository
from .data.stripe.checkout_session_completed import generate_stripe_checkout_session_completed
from andelsbolig.security.service import decode_jwt

user_db = UserRepository()
doc = user_db.read({})
if doc:
    # Find all except superuser with email juliankl1509@gmail.com
    user_db.delete_many({"email": {"$ne": "juliankl1509@gmail.com"}})

# 2 users for tests since it can be handy to test more complex scenarios
client, jwt = generate_subscribed_client("user@example.com")
client2, jwt2 = generate_subscribed_client("user2@example.com")

test_suite_user_id = decode_jwt(jwt).sub
test_suite_user_id2 = decode_jwt(jwt2).sub
