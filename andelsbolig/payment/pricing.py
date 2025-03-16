import stripe

from andelsbolig.config.properties import STRIPE_PRODUCT_ID

product_prices = {
    "3-day-subscription": {"price": 3000, "days_of_access": 3, "interval": "day", "interval_count": 3},
    "monthly-subscription": {"price": 10000, "days_of_access": 31, "interval": "month", "interval_count": 1},
    "semiannual-subscription": {"price": 25000, "days_of_access": 31 * 3, "interval": "month", "interval_count": 3},
}


def find_price_entry_by_amount(price_amount):
    """
    Finds the price entry in the product_prices dictionary that matches the given price amount.

    :param price_amount: int - The price amount in the smallest currency unit (e.g., øre)
    :return: dict or None - The matching price entry or None if no match is found
    """
    for key, value in product_prices.items():
        if value["price"] == price_amount:
            return key, value
    return None


def configure_stripe_pricing():
    # Create a price for every 3 days for 30 kr (3000 øre)

    # Fetch existing prices to avoid duplicates
    existing_prices = stripe.Price.list(product=STRIPE_PRODUCT_ID)
    existing_nickname_prices = {price.nickname: price for price in existing_prices if price.nickname}

    # Create prices if they do not already exist
    for product_name, product_info in product_prices.items():
        if product_name in existing_nickname_prices:
            continue  # Skip creating price if it already exists

        print(f"Creating price for {product_name}")
        stripe.Price.create(
            unit_amount=product_info["price"],
            currency="dkk",
            recurring={"interval": product_info["interval"], "interval_count": product_info["interval_count"]},
            product=STRIPE_PRODUCT_ID,
            nickname=product_name,
        )
