import time
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class AgentCriteria(BaseModel):
    price_from: Optional[int] = None
    price_to: Optional[int] = None
    monthly_price_from: Optional[int] = None
    monthly_price_to: Optional[int] = None
    square_meters_from: Optional[int] = None
    square_meters_to: Optional[int] = None
    rooms_from: Optional[int] = None
    rooms_to: Optional[int] = None
    cities: Optional[List[str]] = None
    postal_numbers: Optional[List[int]] = None
    features: Optional[List[str]] = None  # Additional features like 'balcony', 'pool', etc.
    max_distance_km: Optional[int] = None
    radius: Optional[int] = None


class Agent(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    created: int = Field(default_factory=lambda: int(time.time()))
    updated: int = Field(default_factory=lambda: int(time.time()))
    created_by: str  # Link to user ID who created the agent
    notifications: List[str]  # List of notification types e.g., email, SMS
    active: bool  # Whether the agent is active or not
    criteria: AgentCriteria
    name: Optional[str]


class AgentCreate(BaseModel):
    notifications: List[str] = ["sms", "email"]  # List of notification types e.g., email, SMS
    active: bool = True  # Whether the agent is active or not
    criteria: AgentCriteria
    name: Optional[str]
