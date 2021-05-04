import jwt
import time

from datetime import datetime, timedelta

from app.domain.config import *
from app.dtos import user_dtos


def create_access_token(login_data: user_dtos.Login) -> user_dtos.Token:
    data = {"sub": login_data.email}

    if login_data.expires:
        expire = datetime.utcnow() + timedelta(minutes=login_data.expires)
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=JWT_SIGNING_ALGORITHM)

    token = user_dtos.Token(
        access_token=encoded_jwt,
        token_type="bearer"
    )

    return token


def decode_jwt(token: str) -> dict:

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[JWT_SIGNING_ALGORITHM])
        email = decoded_token.get("sub")
        expiry = decoded_token.get("exp")

        if not email:
            return None

        if expiry < time.time():
            return None

        return decoded_token

    except jwt.PyJWTError:
        return None
