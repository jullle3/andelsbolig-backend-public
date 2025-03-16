import time


def generate_stripe_checkout_session_completed(client_reference_id: str):
    """
    :param client_reference_id: Our internal user id which bought the product
    :return: Mocked Stripe event data for checkout.session.completed
    """
    return {
        "id": "evt_1PiJMURwMNhLL1Z9OYPmUM0q",
        "object": "event",
        "api_version": "2024-06-20",
        "created": int(time.time()),
        "data": {
            "object": {
                "id": "cs_test_a11uiTfrKrYcBFHzDEzxeux2qSGTGNL8UfD9vZvKVoejhykoC5cTQ22Dzu",
                "object": "checkout.session",
                "after_expiration": None,
                "allow_promotion_codes": False,
                "amount_subtotal": 10000,
                "amount_total": 10000,
                "automatic_tax": {"enabled": False, "liability": None, "status": None},
                "billing_address_collection": "auto",
                "cancel_url": "https://stripe.com",
                "client_reference_id": client_reference_id,
                "client_secret": None,
                "consent": None,
                "consent_collection": {
                    "payment_method_reuse_agreement": None,
                    "promotions": "none",
                    "terms_of_service": "none",
                },
                "created": int(time.time()),
                "currency": "dkk",
                "currency_conversion": None,
                "custom_fields": [],
                "custom_text": {
                    "after_submit": None,
                    "shipping_address": None,
                    "submit": None,
                    "terms_of_service_acceptance": None,
                },
                "customer": "cus_QZSG96vNRtOQta",
                "customer_creation": "if_required",
                "customer_details": {
                    "address": {
                        "city": None,
                        "country": "DK",
                        "line1": None,
                        "line2": None,
                        "postal_code": None,
                        "state": None,
                    },
                    "email": "5@gmail.com",
                    "name": "Julletest",
                    "phone": None,
                    "tax_exempt": "none",
                    "tax_ids": [],
                },
                "customer_email": None,
                "expires_at": int(time.time()) + 3600,
                "invoice": "in_1PiJMRRwMNhLL1Z95PB99Lp9",
                "invoice_creation": None,
                "livemode": False,
                "locale": "da",
                "metadata": {},
                "mode": "subscription",
                "payment_intent": None,
                "payment_link": "plink_1Phs2KRwMNhLL1Z9Zcq2hDI2",
                "payment_method_collection": "always",
                "payment_method_configuration_details": {"id": "pmc_1Pi0yPRwMNhLL1Z9kvcMRzlj", "parent": None},
                "payment_method_options": {"card": {"request_three_d_secure": "automatic"}},
                "payment_method_types": ["card", "link", "paypal"],
                "payment_status": "paid",
                "phone_number_collection": {"enabled": False},
                "recovered_from": None,
                "saved_payment_method_options": {
                    "allow_redisplay_filters": ["always"],
                    "payment_method_remove": None,
                    "payment_method_save": None,
                },
                "setup_intent": None,
                "shipping_address_collection": None,
                "shipping_cost": None,
                "shipping_details": None,
                "shipping_options": [],
                "status": "complete",
                "submit_type": "auto",
                "subscription": "sub_1PiJMRRwMNhLL1Z97rouL2Zb",
                "success_url": "https://stripe.com",
                "total_details": {"amount_discount": 0, "amount_shipping": 0, "amount_tax": 0},
                "ui_mode": "hosted",
                "url": None,
            }
        },
        "livemode": False,
        "pending_webhooks": 2,
        "request": {"id": None, "idempotency_key": None},
        "type": "checkout.session.completed",
    }
