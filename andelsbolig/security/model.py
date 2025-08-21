import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class JWT:
    exp: int  # Expiration time (Unix timestamp)
    iat: int  # Issued at time (Unix timestamp)
    iss: str  # Issuer URL
    sub: str  # Subject (user ID aka Mongo _id)
    email: str
    full_name: str
    email_notifications: bool
    sms_notifications: bool
