from __future__ import annotations

import bson
import pymongo

from andelsbolig.advertisement.model import Advertisement, AdvertisementCreate
from andelsbolig.advertisement.repository import AdvertisementRepository
from andelsbolig.config.properties import S3_URL, EARTH_RADIUS_KM
from andelsbolig.geo.geo import postal_dict
from andelsbolig.misc.logger import get_logger
from andelsbolig.security.model import JWT
from andelsbolig.user.repository import UserRepository

db = AdvertisementRepository()
user_db = UserRepository()
logger = get_logger(__name__)


def do_patch_advertisement(patch: dict, jwt: JWT):
    # Ensure doc exists, since it is completely valid for uploads to happen before the user submits the whole form
    if db.read({"created_by": jwt.sub}) is None:
        # Default values to simplify frontend code. Ideally they were set to None and frontend handled those
        db.create(Advertisement(images=[], created_by=jwt.sub, title="", description="", price=0, monthly_fee=0))

    if "url" in patch:
        thumbnail_url = calculate_thumbnail_url(patch["url"])
        urls = {"url": patch["url"], "thumbnail_url": thumbnail_url}
        db.update({"created_by": jwt.sub}, {"$push": {"images": urls}})
        logger.info("Added image to advertisement")


def calculate_thumbnail_url(url: str) -> str:
    """Ideelt skulle dette ikke beregnes her, men sådan er det indtil root cause fikses"""
    filename = url.split(S3_URL)[1][1:]
    thumbnail_url = f"{S3_URL}/thumbnail_{filename}"
    return thumbnail_url


def create_advertisement(advertisement_create: AdvertisementCreate, jwt: JWT) -> Advertisement:
    """
    Create Advertisement instance from AdvertisementCreate
    """
    user = user_db.read({"_id": jwt.sub})

    advertisement = Advertisement(
        images=advertisement_create.images,
        created_by=jwt.sub,
        price=advertisement_create.price,
        monthly_fee=advertisement_create.monthly_fee,
        square_meters=advertisement_create.square_meters,
        rooms=advertisement_create.rooms,
        located_at_top=advertisement_create.located_at_top,
        emails=[user.email],
        phone_numbers=[user.phone_number] if user.phone_number else None,
        title=advertisement_create.title,
        description=advertisement_create.description,
        datafordeler_id=advertisement_create.datafordeler_id,
        location=advertisement_create.location,
        postal_number=advertisement_create.postal_number,
        postal_name=advertisement_create.postal_name,
        street_name=advertisement_create.street_name,
        house_number=advertisement_create.house_number,
        city=advertisement_create.city,
        address=advertisement_create.address,
        floor=advertisement_create.floor,
    )

    # In case user already has an advertisement, we update the existing one
    existing_advertisement = db.read({"created_by": jwt.sub})
    if existing_advertisement:
        advertisement.id = existing_advertisement.id
        advertisement.images = existing_advertisement.images
        advertisement.created = existing_advertisement.created
        advertisement.views = existing_advertisement.views
        advertisement.deleted = existing_advertisement.deleted
        advertisement.visible = existing_advertisement.visible
        advertisement.street_name = existing_advertisement.street_name
        advertisement.house_number = existing_advertisement.house_number
        advertisement.postal_number = existing_advertisement.postal_number
        advertisement.city = existing_advertisement.city

    return advertisement


def build_query(
    text,
    price_from,
    price_to,
    monthly_fee_from,
    monthly_fee_to,
    square_meter_from,
    square_meter_to,
    rooms_from,
    rooms_to,
    radius,
    postal_number,
    city,
    created_by,
):

    query = {}
    # Handling text-based search
    if text:
        regx = bson.regex.Regex(text)
        query |= {
            "$or": [
                {"title": {"$regex": regx, "$options": "i"}},
                {"description": {"$regex": regx, "$options": "i"}},
                {"city": {"$regex": regx, "$options": "i"}},
                {"postal_number": {"$regex": regx, "$options": "i"}},
                {"address": {"$regex": regx, "$options": "i"}},
            ]
        }

    # Handling range-based queries
    if price_from is not None and price_to is not None:
        query |= {"price": {"$gte": price_from, "$lte": price_to}}
    if monthly_fee_from is not None and monthly_fee_to is not None:
        query |= {"monthly_fee": {"$gte": monthly_fee_from, "$lte": monthly_fee_to}}
    if square_meter_from is not None and square_meter_to is not None:
        query |= {"square_meters": {"$gte": square_meter_from, "$lte": square_meter_to}}
    if rooms_from is not None and rooms_to is not None:
        query |= {"rooms": {"$gte": rooms_from, "$lte": rooms_to}}

    if radius is not None and postal_number is not None:
        if postal_number in postal_dict:
            postal_record = postal_dict[postal_number]
            # 1. Convert the radius from kilometers to radians
            radius_in_radians = radius / EARTH_RADIUS_KM

            # 2. Build the $geoWithin + $centerSphere query
            query |= {
                "location": {
                    "$geoWithin": {"$centerSphere": [[postal_record.long, postal_record.lat], radius_in_radians]}
                }
            }

    # Filtering by postal number or city
    if postal_number:
        query |= {"postal_number": postal_number}
    if city:
        query |= {"city": city}

    # Filtering by creator
    if created_by:
        query |= {"created_by": created_by}

    return query


def calculate_sorting(sort: str | None):
    if not sort:
        return None, None

    # Given a request from frontend, calculate the actual sorting field and direction
    field = sort.split("-")[0]
    ascending = pymongo.ASCENDING if sort.split("-")[1].lower() == "asc" else pymongo.DESCENDING

    return field, ascending


