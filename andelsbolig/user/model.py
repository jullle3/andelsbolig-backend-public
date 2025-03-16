import time
from typing import Optional

from bson import ObjectId
from pydantic import EmailStr, BaseModel, Field, field_validator


class User(BaseModel):
    """Model stored in DB"""

    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    created: int = Field(default_factory=lambda: int(time.time()))
    updated: int = Field(default_factory=lambda: int(time.time()))
    email: str
    password_hash: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    last_login: Optional[int] = None
    subscription_expiration: Optional[int] = None  # Timestamp of when the subscription expires
    email_notifications: bool = True
    sms_notifications: bool = True
    favorite_advertisements: list = []
    # stripe_id: Optional[str] = None  # Stripe customer id

    def is_subscribed(self) -> bool:
        """Returns True if the current time is less than the subscription expiration time."""
        return self.subscription_expiration is not None and self.subscription_expiration > time.time()


class UserCreate(BaseModel):
    """Model received from frontend"""

    email: EmailStr
    password: str
    full_name: str
    phone_number: Optional[str] = None

    @field_validator("email")
    def lowercase_email(cls, v):
        return v.lower()

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Adgangskode skal være mindst 8 tegn lang")
        return v

    @field_validator("full_name")
    def validate_full_name(cls, v):
        if not v.strip():
            raise ValueError("Fulde navn må ikke være tomt")
        if len(v) > 50:
            raise ValueError("Fulde navn må ikke overstige 50 tegn")
        return v

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        if v and not v.isdigit():
            raise ValueError("Telefonnummer skal kun indeholde cifre")
        return v


class LoginCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    def lowercase_email(cls, v):
        return v.lower()


class PatchUserRequest(BaseModel):
    email_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None
    favorite_advertisement_add_operation: Optional[bool] = None
    favorite_advertisement: Optional[str] = None
