import json

import stripe
from fastapi import APIRouter
from fastapi import Request, HTTPException

from andelsbolig.config.properties import STRIPE_ENDPOINT_SECRET
from andelsbolig.misc.logger import get_logger
from andelsbolig.payment.service import (
    handle_checkout_session_completed,
)

router = APIRouter()
logger = get_logger(__name__)


@router.post("/webhook")
async def webhook(request: Request):
    """
    Handle Stripe webhooks
    """
    sig_header = request.headers.get("stripe-signature")
    payload = await request.body()

    # Debugging purposes
    decoded_string = payload.decode("utf-8")
    stripe_event_data = json.loads(decoded_string)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_ENDPOINT_SECRET)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event.type == "checkout.session.completed":
        handle_checkout_session_completed(event.data.object)
    # elif event.type == "customer.subscription.updated":
    #     handle_customer_subscription_updated(event.data.object)
    # elif event.type == "customer.created":
    #     handle_customer_created(event.data.object)
