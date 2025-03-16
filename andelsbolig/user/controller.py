import hashlib
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends

from andelsbolig.misc.logger import get_logger
from andelsbolig.security.service import create_jwt, is_subscribed, is_authenticated
from andelsbolig.user.model import UserCreate, User, LoginCreate, PatchUserRequest
from andelsbolig.user.repository import UserRepository

router = APIRouter()
db = UserRepository()
logger = get_logger(__name__)


@router.patch("/user")
def patch_user(patch_user_request: PatchUserRequest, jwt=Depends(is_authenticated)):
    """Update part of the user document"""
    if (
        patch_user_request.email_notifications is None
        and patch_user_request.sms_notifications is None
        and patch_user_request.favorite_advertisement is None
    ):
        raise HTTPException(status_code=400, detail="Ingen felter at opdatere")

    # Set operations
    if patch_user_request.email_notifications is not None and patch_user_request.sms_notifications is not None:
        update = {}
        if patch_user_request.email_notifications is not None:
            update["email_notifications"] = patch_user_request.email_notifications
        if patch_user_request.sms_notifications is not None:
            update["sms_notifications"] = patch_user_request.sms_notifications
        db.update({"_id": jwt.sub}, {"$set": update})
    # array operations
    else:
        if patch_user_request.favorite_advertisement_add_operation:
            operation = "$addToSet"
        else:
            operation = "$pull"
        db.update({"_id": jwt.sub}, {operation: {"favorite_advertisements": patch_user_request.favorite_advertisement}})


@router.post("/user")
def create_user(user_create: UserCreate):
    """Create user and return JWT upon success"""
    if db.exists({"email": user_create.email}, 1):
        raise HTTPException(status_code=400, detail="Email eksisterer allerede")

    hashed_password = get_password_hash(user_create.password)

    user = User(
        email=str(user_create.email),
        password_hash=hashed_password,
        full_name=user_create.full_name,
        phone_number=user_create.phone_number,
    )

    db.create(user)

    jwt = create_jwt(user_create.email)

    return {"jwt": jwt}


@router.post("/login")
async def login(login_create: LoginCreate):
    user = db.read({"email": login_create.email})
    if not user or not verify_password(login_create.password, user.password_hash):
        raise HTTPException(
            status_code=401, detail="Vi kunne ikke finde en bruger der matchede. Prøv igen med en ny email eller kode."
        )

    user.last_login = datetime.utcnow()
    db.update({"email": user.email}, {"$set": {"last_login": user.last_login}})

    jwt = create_jwt(user.email)
    return {"jwt": jwt}


@router.get("/user/{_id}")
def get_user(_id: str, _=Depends(is_subscribed)) -> User:
    user = db.read({"_id": _id})
    if user is None:
        raise HTTPException(status_code=404, detail="Brugeren findes ikke")

    # Scramble fields that in reality shouldn't be returned here
    user.password_hash = "x"
    user.subscription_expiration = 0
    return user


def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password, hashed_password) -> bool:
    return hashed_password == get_password_hash(plain_password)
