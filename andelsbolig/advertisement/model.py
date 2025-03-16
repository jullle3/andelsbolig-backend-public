import re
import time
from typing import Optional, List

import requests
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, model_validator

from andelsbolig.config.properties import DATAFORDELER_API
from andelsbolig.util import parse_long_lat


class ImageUrl(BaseModel):
    url: str
    thumbnail_url: str


class Advertisement(BaseModel):
    # Auto-generated fields
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    created: int = Field(default_factory=lambda: int(time.time()))
    updated: int = Field(default_factory=lambda: int(time.time()))

    # User input fields
    images: List[dict] = []
    created_by: str  # Link to user ID
    price: Optional[int] = None
    monthly_fee: Optional[int] = None
    square_meters: Optional[int] = None
    rooms: Optional[int] = None
    located_at_top: Optional[bool] = None
    emails: Optional[List[EmailStr]] = None
    phone_numbers: Optional[List[str]] = None
    title: Optional[str] = None
    description: Optional[str] = None
    # Address data
    datafordeler_id: Optional[str] = None
    location: Optional[dict] = None
    postal_number: Optional[int] = None
    postal_name: Optional[str] = None
    street_name: Optional[str] = None
    house_number: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    floor: Optional[str] = None

    # System fields
    views: int = 0
    deleted: bool = False
    visible: bool = True
    # List of agents that have been notified about this advertisement
    notified_agents: List[str] = []

    # TODO: Autogenerate these with OpenAI
    # @model_validator(mode="after")
    # def set_values(cls, values):
    # values.title = "foo"
    # values.description = "foo"


class AdvertisementCreate(BaseModel):
    """User input model"""

    title: str
    description: str
    price: int
    monthly_fee: int
    square_meters: int
    rooms: int
    images: List[dict] = []
    located_at_top: bool

    # Address data
    datafordeler_id: Optional[str] = None
    location: Optional[dict] = None
    postal_number: Optional[int] = None
    postal_name: Optional[str] = None  # Eksempelvis Dyssegård
    street_name: Optional[str] = None
    house_number: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    floor: Optional[str] = None

    @model_validator(mode="after")
    def validate_address(cls, model):
        if not model.datafordeler_id:
            return model

        params = {"Format": "JSON", "id": model.datafordeler_id}

        response = requests.get(DATAFORDELER_API + "/adresse", params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        address_metadata = response.json()[0]
        point_str = address_metadata["husnummer"]["adgangspunkt"]["position"]
        # Coordinate extraction from the 'POINT' string
        matches = re.findall(r"[\d.]+", point_str)
        easting = float(matches[0])
        northing = float(matches[1])
        long, lat = parse_long_lat(easting, northing)
        model.location = {"type": "Point", "coordinates": [long, lat]}
        model.address = address_metadata["adressebetegnelse"]
        model.floor = address_metadata["etagebetegnelse"]
        model.postal_number = address_metadata["husnummer"]["postnummer"]["postnr"]
        model.postal_name = address_metadata["husnummer"]["postnummer"]["navn"]
        model.street_name = address_metadata["husnummer"]["navngivenVej"]["vejnavn"]
        model.house_number = address_metadata["husnummer"]["husnummertekst"]
        model.city = address_metadata["husnummer"]["kommuneinddeling"]["navn"]
        return model
