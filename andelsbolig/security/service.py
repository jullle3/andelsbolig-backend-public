from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Request

from andelsbolig.config.properties import JWT_SECRET, JWT_ALGORITHM
from andelsbolig.security.model import JWT
from andelsbolig.user.repository import UserRepository

user_db = UserRepository()


def decode_jwt(token: str, verify=True) -> JWT:
    """
    :param token: JWT to decode
    :param verify: Whether the JWT signature should be cryptographically verified
    :return:
    """
    try:
        # Decode the JWT using the secret key and the specified algorithm
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], options={"verify_signature": verify})
        return JWT(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token is invalid")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


def extract_jwt(request: Request):
    # Extract the token from the Authorization header
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        return token[7:]  # Strip "Bearer " to get the actual token
    else:
        raise HTTPException(
            status_code=401, detail="Vi kunne ikke bekræfte din adgang. Sørg for, at du er logget ind, og prøv igen."
        )


def create_jwt(email: str):
    user = user_db.read({"email": email})

    issued_at = datetime.utcnow()
    expires_at = issued_at + timedelta(days=365)

    payload = {
        "iss": "https://andelsboligbasen.dk",  # Issuer of the JWT
        "sub": user.id,  # Subject of the JWT (e.g., user ID)
        "iat": issued_at,  # Issued at time
        "exp": expires_at,  # Expiration time of JWT
        "full_name": user.full_name,
        "email": user.email,
        "email_notifications": user.email_notifications,
        "sms_notifications": user.sms_notifications,
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def is_authenticated(request: Request) -> JWT:
    return decode_jwt(extract_jwt(request), verify=True)


def is_subscribed(request: Request) -> JWT:
    jwt_ = decode_jwt(extract_jwt(request), verify=True)
    user = user_db.read({"email": jwt_.email})

    if not user.is_subscribed():
        raise HTTPException(
            status_code=403,
            detail="Det ser ud til, at du ikke har et aktivt abonnement. Kontakt venligst support, hvis du har brug for hjælp.",
        )

    return jwt_


def is_authorized(user_id, stored_user_id):
    """Check if the user is authorized to perform the action"""
    if user_id != stored_user_id:
        raise HTTPException(
            status_code=403,
            detail="Du har ikke tilladelse til at foretage denne handling",
        )
