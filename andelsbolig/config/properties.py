import os

import stripe
from dotenv import load_dotenv

from definitions import ROOT_DIR

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{ROOT_DIR}/s3-service-account.json"

# Bruges for at enable/disable visse funktionaliteter (eks s3 upload)
RUNNING_TESTS = False if os.getenv("RUNNING_TESTS", "FALSE").upper() == "FALSE" else True
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = "HS256"
BUCKET_NAME = "andelsboligbasen"
S3_URL = f"https://storage.googleapis.com/{BUCKET_NAME}"
FRONTEND_URL = os.environ["FRONTEND_URL"]
THUMBNAIL_URL = os.environ["THUMBNAIL_URL"]

STRIPE_SECRET_KEY = os.environ["STRIPE_SECRET_KEY"]
STRIPE_PRODUCT_ID = os.environ["STRIPE_PRODUCT_ID"]
STRIPE_ENDPOINT_SECRET = os.environ["STRIPE_ENDPOINT_SECRET"]
DISABLE_ACCESS_LOGS = False if os.getenv("DISABLE_ACCESS_LOGS", "FALSE").upper() == "FALSE" else True
stripe.api_key = STRIPE_SECRET_KEY
GMAIL_PASSWORD = os.environ["GMAIL_PASSWORD"]
# Datafordeler docs
# https://confluence.sdfi.dk/pages/viewpage.action?pageId=16056323
DATAFORDELER_API = "https://services.datafordeler.dk/DAR/DAR/3.0.0/rest"
EARTH_RADIUS_KM = 6378.1
WORKERS = int(os.getenv("WORKERS", "2"))



