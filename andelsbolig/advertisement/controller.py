from typing import Optional

from fastapi import Query, APIRouter, Depends, HTTPException, Request

from andelsbolig.advertisement.model import Advertisement, AdvertisementCreate
from andelsbolig.advertisement.repository import AdvertisementRepository
from andelsbolig.advertisement.service import (
    do_patch_advertisement,
    create_advertisement,
    build_query, calculate_sorting,
)
from andelsbolig.misc.logger import get_logger
from andelsbolig.security.service import is_authenticated, is_subscribed, decode_jwt, extract_jwt
from andelsbolig.user.repository import UserRepository

router = APIRouter()
db = AdvertisementRepository()
user_db = UserRepository()
logger = get_logger(__name__)


@router.get("/advertisement/{_id}")
# def get_advertisement(_id: str, _=Depends(is_subscribed)) -> Advertisement:
def get_advertisement(_id: str) -> Advertisement:
    """
    Retrieve an advertisement and increment the view count.

    Not to be used for internal calls as it increments the view count.
    """
    # Increment views atomically and return the updated document
    advertisement = db.read_and_update(
        {"_id": _id},
        {"$inc": {"views": 1}},
    )
    if not advertisement:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return advertisement


# TODO: Hvis brugeren sender query med favorites_only=true og uden JWT, så bare ignore det param
@router.get("/advertisement")
def get_advertisement_paged(
    request: Request,
    text: Optional[str] = Query(None),
    price_from: Optional[int] = Query(None),
    price_to: Optional[int] = Query(None),
    monthly_fee_from: Optional[int] = Query(None),
    monthly_fee_to: Optional[int] = Query(None),
    square_meter_from: Optional[int] = Query(None),
    square_meter_to: Optional[int] = Query(None),
    rooms_from: Optional[int] = Query(None),
    rooms_to: Optional[int] = Query(None),
    radius: Optional[int] = Query(None),
    postal_number: Optional[int] = Query(None),
    city: Optional[str] = Query(None),
    page: Optional[int] = Query(0),
    size: Optional[int] = Query(20),
    created_by: Optional[str] = Query(None),
    count_only: Optional[bool] = Query(None),
    favorites_only: Optional[bool] = Query(None),
    sort: Optional[str] = Query(None),
):
    query = build_query(
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
    )

    # Get users favorite advertisements
    if favorites_only:
        token = request.headers.get("Authorization")
        if token:
            jwt_ = decode_jwt(extract_jwt(request), verify=True)
            user = user_db.read({"email": jwt_.email})
            if user:
                query |= {'_id': {"$in": user.favorite_advertisements}}

    field, direction = calculate_sorting(sort)
    page = db.read_paged(query, page, size, field, direction)

    if count_only:
        del page["objects"]
    return page


@router.post("/advertisement")
def post_advertisement(advertisement_create: AdvertisementCreate, jwt=Depends(is_authenticated)) -> str:
    advertisement = create_advertisement(advertisement_create, jwt)
    db.replace(advertisement, upsert=True)
    return advertisement.id


# @router.put("/advertisement")
# def put_advertisement(advertisement_create: AdvertisementCreate):
#     db.replace({"_id": advertisement_create["_id"]}, advertisement_create)


@router.patch("/advertisement")
def patch_advertisement(patch: dict, jwt=Depends(is_authenticated)):
    do_patch_advertisement(patch, jwt)


# TODO. Should probably never fully delete advertisements, only mark them as deleted
# @router.delete("/advertisement/{_id}")
# def delete_advertisement(_id, jwt=Depends(is_authenticated)):
#     db.delete({"_id": _id, "created_by": jwt.sub})


# @router.get("/advertisement_atlas")
# def get_advertisement_atlas(
#         _id: Optional[str] = Query(None),
#         text: Optional[str] = Query(None),
#         page: Optional[int] = Query(0),
#         size: Optional[int] = Query(20),
# ):
#     """
#     TODO: Indeholder queries som åbenbart kun kan bruges i atlas
#     """
#
#     if _id is None and text is None:
#         raise HTTPException(status_code=400, detail="At least one of _id or text must be provided.")
#
#     t1 = time.time()
#
#     # _id is unique
#     if _id:
#         advertisement = db.read({"_id": _id})
#         page = {"objects": advertisement, "total_object_count": 1, "count": 1}
#     else:
#         # Add stages to aggregation
#         aggregation = [
#             {
#                 "$search": {
#                     "index": "search_index",
#                     "text": {"query": text, "path": ["title", "description", "city", "postal_number", "address"]},
#                 }
#             }
#         ]
#
#         aggregation.extend(
#             [
#                 {"$skip": page * size},
#                 {"$limit": size},
#                 {"$facet": {"metadata": [{"$count": "total"}], "data": [{"$addFields": {"id": "$_id"}}]}},
#                 {"$unwind": "$metadata"},
#                 {"$project": {"data": 1, "total_object_count": "$metadata.total"}},
#             ]
#         )
#         results = db.read_paged_aggregation(aggregation)
#
#     logger.debug(
#         f"found {len(page['objects'])}/{page['total_object_count']} docs in {round(time.time() - t1, 6)} seconds"
#     )
#
#     return page
