import hashlib
import string

from sqlalchemy.orm.session import Session
from app.commonhelper import utils

from app.data import models
from app.data.enums import UserTokenType
from app.domain.config import USER_TOKEN_RESET_PASSWORD_EXPIRE_MINUTES, USER_TOKEN_RESET_PASSWORD_LENGTH
from app.domain.constants import FORGOT_PASSWORD_TEMPLATE
from app.dtos import auth_dtos, user_dtos
from app.mappings.user_mappings import user_to_user_response
from app.services import email_service, user_service, user_token_service


def get_user_password(db: Session, username: str) -> auth_dtos.Password:

    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        return None

    response = auth_dtos.Password(
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


def authenticate_user(db: Session, username: str, password: str) -> bool:
    user_password = get_user_password(db, username)

    if not user_password:
        return False

    if not verify_password(password, user_password.password_hash, user_password.password_salt):
        return False

    return True


def forgot_password(db: Session, forgot_password_data: auth_dtos.ForgotPassword) -> None:
    user = user_service.get_user_by_username(db, forgot_password_data.username)

    user_token = user_token_service.generate_token(db, USER_TOKEN_RESET_PASSWORD_LENGTH, string.ascii_letters, USER_TOKEN_RESET_PASSWORD_EXPIRE_MINUTES, UserTokenType.RESET_PASSWORD, user.id)

    payload = {
        "token": user_token.token
    }

    email_service.send_email(forgot_password_data.email, FORGOT_PASSWORD_TEMPLATE, payload)


def reset_password(db: Session, reset_password_data: auth_dtos.ResetPassword) -> user_dtos.UserResponse:
    user = user_service.get_user_by_username(db, reset_password_data.username)

    user_token_service.use_token(db, user.id, reset_password_data.token, UserTokenType.RESET_PASSWORD)

    password_hash, password_salt = utils.generate_hash_and_salt(reset_password_data.password)

    user.password_hash = password_hash
    user.password_salt = password_salt

    db.commit()
    db.refresh(user)

    return user_to_user_response(user)
