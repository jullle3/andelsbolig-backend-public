stripe_customer_subscription_updated = {
    "api_version": "2024-06-20",
    "created": 1722290054,
    "data": {
        "object": {
            "application": None,
            "application_fee_percent": None,
            "automatic_tax": {"enabled": False, "liability": None},
            "billing_cycle_anchor": 1722290051,
            "billing_cycle_anchor_config": None,
            "billing_thresholds": None,
            "cancel_at": None,
            "cancel_at_period_end": False,
            "canceled_at": None,
            "cancellation_details": {"comment": None, "feedback": None, "reason": None},
            "collection_method": "charge_automatically",
            "created": 1722290051,
            "currency": "usd",
            "current_period_end": 1724968451,
            "current_period_start": 1722290051,
            "customer": "cus_QZ9p2Pa5JQTgj9",
            "days_until_due": None,
            "default_payment_method": None,
            "default_source": None,
            "default_tax_rates": [],
            "description": None,
            "discount": None,
            "discounts": [],
            "ended_at": None,
            "id": "sub_1Pi1WBRwMNhLL1Z9vWhSJvr7",
            "invoice_settings": {"account_tax_ids": None, "issuer": {"type": "self"}},
            "items": {
                "data": [
                    {
                        "billing_thresholds": None,
                        "created": 1722290051,
                        "discounts": [],
                        "id": "si_QZ9pz43RgZzZL9",
                        "metadata": {},
                        "object": "subscription_item",
                        "plan": {
                            "active": True,
                            "aggregate_usage": None,
                            "amount": 1500,
                            "amount_decimal": "1500",
                            "billing_scheme": "per_unit",
                            "created": 1722290050,
                            "currency": "usd",
                            "id": "price_1Pi1WARwMNhLL1Z9eqFI0W7l",
                            "interval": "month",
                            "interval_count": 1,
                            "livemode": False,
                            "metadata": {},
                            "meter": None,
                            "nickname": None,
                            "object": "plan",
                            "product": "prod_QZ9p1sm5aASslZ",
                            "tiers_mode": None,
                            "transform_usage": None,
                            "trial_period_days": None,
                            "usage_type": "licensed",
                        },
                        "price": {
                            "active": True,
                            "billing_scheme": "per_unit",
                            "created": 1722290050,
                            "currency": "usd",
                            "custom_unit_amount": None,
                            "id": "price_1Pi1WARwMNhLL1Z9eqFI0W7l",
                            "livemode": False,
                            "lookup_key": None,
                            "metadata": {},
                            "nickname": None,
                            "object": "price",
                            "product": "prod_QZ9p1sm5aASslZ",
                            "recurring": {
                                "aggregate_usage": None,
                                "interval": "month",
                                "interval_count": 1,
                                "meter": None,
                                "trial_period_days": None,
                                "usage_type": "licensed",
                            },
                            "tax_behavior": "unspecified",
                            "tiers_mode": None,
                            "transform_quantity": None,
                            "type": "recurring",
                            "unit_amount": 1500,
                            "unit_amount_decimal": "1500",
                        },
                        "quantity": 1,
                        "subscription": "sub_1Pi1WBRwMNhLL1Z9vWhSJvr7",
                        "tax_rates": [],
                    }
                ],
                "has_more": False,
                "object": "list",
                "total_count": 1,
                "url": "/v1/subscription_items?subscription=sub_1Pi1WBRwMNhLL1Z9vWhSJvr7",
            },
            "latest_invoice": "in_1Pi1WBRwMNhLL1Z9mSQDnR7t",
            "livemode": False,
            "metadata": {"foo": "bar"},
            "next_pending_invoice_item_invoice": None,
            "object": "subscription",
            "on_behalf_of": None,
            "pause_collection": None,
            "payment_settings": {
                "payment_method_options": None,
                "payment_method_types": None,
                "save_default_payment_method": "off",
            },
            "pending_invoice_item_interval": None,
            "pending_setup_intent": None,
            "pending_update": None,
            "plan": {
                "active": True,
                "aggregate_usage": None,
                "amount": 1500,
                "amount_decimal": "1500",
                "billing_scheme": "per_unit",
                "created": 1722290050,
                "currency": "usd",
                "id": "price_1Pi1WARwMNhLL1Z9eqFI0W7l",
                "interval": "month",
                "interval_count": 1,
                "livemode": False,
                "metadata": {},
                "meter": None,
                "nickname": None,
                "object": "plan",
                "product": "prod_QZ9p1sm5aASslZ",
                "tiers_mode": None,
                "transform_usage": None,
                "trial_period_days": None,
                "usage_type": "licensed",
            },
            "quantity": 1,
            "schedule": None,
            "start_date": 1722290051,
            "status": "active",
            "test_clock": None,
            "transfer_data": None,
            "trial_end": None,
            "trial_settings": {"end_behavior": {"missing_payment_method": "create_invoice"}},
            "trial_start": None,
        },
        "previous_attributes": {"metadata": {"foo": None}},
    },
    "id": "evt_1Pi1WERwMNhLL1Z9FKdIDVBl",
    "livemode": False,
    "object": "event",
    "pending_webhooks": 2,
    "request": {"id": "req_NR5rTxLoEMeLkM", "idempotency_key": "30acca1d-93ff-4499-9bf8-ec6a9039c732"},
    "type": "customer.subscription.updated",
}
