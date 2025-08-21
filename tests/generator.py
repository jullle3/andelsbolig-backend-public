import hashlib
import hmac
import json
import random
import time

from bson import ObjectId
from starlette.testclient import TestClient

import andelsbolig
from andelsbolig.agent.model import AgentCreate, AgentCriteria
from andelsbolig.config.properties import STRIPE_ENDPOINT_SECRET
from andelsbolig.comment_thread.model import CommentCreate
from andelsbolig.user.model import UserCreate, User
from andelsbolig.user.repository import UserRepository
from tests.data.data import cities
from tests.data.stripe.checkout_session_completed import generate_stripe_checkout_session_completed

user_db = UserRepository()


def generate_random_address() -> str:
    streets = ["Østerbrogade", "Nørrebrogade", "Vesterbrogade", "Amagerbrogade", "Frederiksborggade"]
    number = random.randint(1, 200)
    return f"{random.choice(streets)} {number}"


def generate_random_title() -> str:
    adjectives = ["Luksuriøs", "Komfortabel", "Charmerende", "Moderne", "Rummelig"]
    nouns = ["lejlighed", "villa", "penthouse", "et værelses", "familiehus"]
    return f"{random.choice(adjectives)} {random.choice(nouns)} i hjertet af København"


def generate_random_description() -> str:
    features = [
        "et badeværelse med moderne faciliteter",
        "et nyligt renoveret køkken med alle nødvendige apparater",
        "en lys stue med store vinduer, der giver udsigt over byen",
        "en stor altan perfekt til hyggelige aftener og morgenkaffe",
        "en rummelig spisestue, der egner sig godt til familiesammenkomster",
        "et soveværelse med indbyggede skabe og masser af naturligt lys",
        "en hyggelig baghave med plads til grill og udendørs aktiviteter",
        "en garage med plads til to biler og opbevaring",
        "nærhed til skole, supermarked og offentlig transport",
        "et roligt nabolag med grønne områder og legepladser",
    ]

    # List of introductory phrases
    introductions = [
        "Velkommen til dette dejlige hjem, som tilbyder",
        "Oplev komfort og bekvemmelighed i dette skønne hjem, der har",
        "Dette fantastiske hjem byder på",
        "Gør dig klar til at blive imponeret af",
        "Dette hjem er perfekt til både familier og enkeltpersoner, og tilbyder",
    ]

    # Select a few features to include in the description
    selected_features = random.sample(features, k=3)

    # Select a random introductory phrase
    introduction = random.choice(introductions)

    # Construct a more detailed and flowing description
    description = (
        f"{introduction} {selected_features[0]}. "
        f"Derudover har boligen {selected_features[1]} og {selected_features[2]}. "
        "Dette hjem er perfekt til både familier og enkeltpersoner, der ønsker komfort "
        "og bekvemmelighed i en skøn beliggenhed."
    )

    return description


def generate_random_city() -> str:
    cities = ["København", "Aarhus", "Odense", "Aalborg", "Esbjerg", "Randers", "Vejle"]
    return random.choice(cities)


def get_random_modified_coordinates():
    """
    Selects a random city from the list and modifies its coordinates slightly.
    This is such that not all advertisements are placed in the exact same location when testing
    """
    # Choose a random city
    selected_city = random.choice(cities)
    original_lon, original_lat = selected_city["coordinates"]

    # Apply a small random change to longitude and latitude
    # This change is within ±0.0100 degrees, which corresponds to a variance of about 1000 meters
    modified_lon = original_lon + random.uniform(-0.0100, 0.0100)
    modified_lat = original_lat + random.uniform(-0.0100, 0.0100)

    return modified_lon, modified_lat


def generate_advertisement_create() -> dict:
    long, lat = get_random_modified_coordinates()
    return {
        "title": generate_random_title(),
        "description": generate_random_description(),
        "price": random.randint(1_000_000, 5_000_000),
        "monthly_fee": random.randint(3000, 7000),
        "square_meters": random.randint(50, 150),
        "rooms": random.randint(1, 5),
        "images": [],
        "located_at_top": random.choice([True, False]),
        # It actually points to a real address in the database, as seen here
        # https://services.datafordeler.dk/DAR/DAR/3.0.0/rest/adresse?Format=JSON&id=0a3f50a3-f563-32b8-e044-0003ba298018
        # "datafordeler_id": "0a3f50a3-f563-32b8-e044-0003ba298018",
        "location": {"type": "Point", "coordinates": [long, lat]},
    }


def generate_agent_create() -> AgentCreate:
    return AgentCreate(notifications=["sms", "email"], criteria=AgentCriteria(cities=["København"]), name="Test Agent")


def generate_user() -> User:
    return User(
        email="example@example.com",
        password_hash="passwordhash",
        full_name="Test User",
        phone_number="12345678",
    )


def generate_user_create(email: str) -> UserCreate:
    return UserCreate(
        email=email,
        password="password",
        full_name="Test User",
        phone_number="12345678",
    )


def generate_comment_create(text: str, reference_id: str) -> CommentCreate:
    return CommentCreate(text=text, referenced_id=reference_id)


def generate_stripe_signed_payload(payload):
    """
    Emulate a stripe HTTP request/webhook by signing payload using Stripe's webhook secret key
    """
    timestamp = int(time.time())
    # Create a payload string based on Stripe's requirements
    signed_payload = f"{timestamp}.{payload}"

    # Create a signature using HMAC-SHA256
    signature = hmac.new(
        key=STRIPE_ENDPOINT_SECRET.encode(), msg=signed_payload.encode(), digestmod=hashlib.sha256
    ).hexdigest()

    # Construct the header in the format Stripe expects
    stripe_signature = f"t={timestamp},v1={signature}"
    return stripe_signature


def generate_subscribed_client(email):
    """Create a new user and subscribe them, thereby authorizing their client"""
    client = TestClient(andelsbolig.app)

    user_create = generate_user_create(email)
    r1 = client.post("/user", json=user_create.model_dump())
    jwt = r1.json()["jwt"]
    client.headers = {"Authorization": f"Bearer {jwt}"}

    # Payment is handled directly via GUI and Stripe, and thus we mock the "checkout.session.completed" which Stripe sends directly
    user_id = user_db.read({"email": email}).id
    mock = generate_stripe_checkout_session_completed(user_id)
    headers = {"stripe-signature": generate_stripe_signed_payload(json.dumps(mock))}
    r2 = client.post("/webhook", json=mock, headers=headers)

    return client, jwt
