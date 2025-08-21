import stripe
from stripe import Subscription, Customer
from stripe.checkout import Session

from andelsbolig.misc.logger import get_logger
from andelsbolig.payment.pricing import find_price_entry_by_amount
from andelsbolig.user.model import User
from andelsbolig.user.repository import UserRepository

user_db = UserRepository()
logger = get_logger(__name__)


def handle_checkout_session_completed(session: Session):
    """
    This function is called when a checkout session is successfully completed, aka customer has paid

    Stripe docs: https://docs.stripe.com/api/events/types#event_types-checkout.session.completed
    """
    user_id = session.client_reference_id
    price_name, price_obj = find_price_entry_by_amount(session.amount_total)
    added_subscription_seconds = price_obj["days_of_access"] * 24 * 60 * 60
    subscription_expiration = session.created + added_subscription_seconds
    user_db.update({"_id": user_id}, {"$set": {"subscription_expiration": subscription_expiration}})

    logger.info(f"User {user_id} has successfully paid for a {price_name}")


def handle_customer_subscription_updated(subscription: Subscription):
    """
    This function is called when a customer subscription is updated, aka customer has paid or cancelled

    Stripe docs: https://docs.stripe.com/api/events/types#event_types-customer.subscription.updated
    # TODO: Mangler ID
    """
    price = stripe.Price.retrieve(subscription.plan.id)

    customer_stripe_id = subscription.customer
    price = subscription.plan.amount
    product = subscription.plan.product
    status = subscription.status


def handle_customer_created(customer: Customer):
    """
    This function is called when a customer is created

    Stripe docs: https://docs.stripe.com/api/customers/object

    """
    # customer_stripe_id = subscription.customer
    # price = subscription.plan.amount
    # product = subscription.plan.product
    # status = subscription.status
    pass


def create_stripe_customer(user: User) -> Customer:
    # Create a new customer in Stripe
    customer = stripe.Customer.create(
        email=user.email, name=user.full_name, description=f"Customer for {user.id} ({user.email})"
    )
    return customer
