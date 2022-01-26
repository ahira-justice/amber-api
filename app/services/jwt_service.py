import jwt
import time

from datetime import datetime, timedelta

from app.domain.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SIGNING_ALGORITHM, SECRET_KEY
from app.dtos import auth_dtos, user_dtos


def create_access_token(create_token_data: auth_dtos.CreateToken) -> auth_dtos.Token:
    data = {"sub": create_token_data.username}

    if create_token_data.expires:
        expire = datetime.utcnow() + timedelta(minutes=create_token_data.expires)
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=JWT_SIGNING_ALGORITHM)

    token = auth_dtos.Token(
        access_token=encoded_jwt,
        token_type="bearer"
    )

    return token


def decode_jwt(token: str) -> dict:

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[JWT_SIGNING_ALGORITHM])
        username = decoded_token.get("sub")
        expiry = decoded_token.get("exp")

        if not username:
            return {}

        if expiry < time.time():
            return {}

        return decoded_token

    except jwt.PyJWTError:
        return {}
