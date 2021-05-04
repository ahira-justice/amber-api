import hashlib

from base64 import b64decode
from pydantic import EmailStr
from sqlalchemy.orm.session import Session

from app.domain.config import *
from app.domain.database import SessionLocal
from app.data import models
from app.dtos import user_dtos


def get_user_password(db: Session, email: EmailStr) -> user_dtos.Password:

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        return None

    response = user_dtos.Password(
        password_hash=user.password_hash,
        password_salt=user.password_salt
    )

    return response


def verify_password(password, password_hash, password_salt) -> bool:
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        password_salt,
        100000,
        dklen=128
    )

    return key == password_hash


def authenticate_user(db: Session, email: str, password: str) -> bool:
    user_password = get_user_password(db, email)

    if not user_password:
        return False

    if not verify_password(password, user_password.password_hash, user_password.password_salt):
        return False

    return True
