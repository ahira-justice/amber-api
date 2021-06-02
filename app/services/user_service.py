from datetime import datetime, timedelta
from fastapi import Request
from pydantic import EmailStr
from sqlalchemy.orm.session import Session
from typing import List

from app.data import models
from app.domain.config import *
from app.domain.constants import *
from app.dtos import user_dtos
from app.commonhelper import utils
from app.exceptions.app_exceptions import BadRequestException, ForbiddenException, NotFoundException
from app.mappings.user_mappings import *
from app.services import email_service, jwt_service


def create_user(db: Session, user_data: user_dtos.UserCreate) -> user_dtos.UserResponse:

    user = user_create_to_user(user_data)

    db.add(user)
    db.commit()
    db.refresh(user)

    response = user_to_user_response(user)

    return response


def create_social_user(db: Session, external_login_data: user_dtos.ExternalLogin) -> user_dtos.UserResponse:

    user = external_login_to_user(external_login_data)

    db.add(user)
    db.commit()
    db.refresh(user)

    response = user_to_user_response(user)

    return response


def seed_user(db: Session, email: EmailStr, first_name: str, last_name: str, password: str) -> user_dtos.UserResponse:

    payload = user_dtos.UserCreate(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password
    )

    admin_user = create_user(db, payload)
    return admin_user


def set_super_admin(db: Session, id: int):

    user = db.query(models.User).filter(models.User.id == id).first()
    user.is_admin = True
    user.is_staff = True

    db.commit()
    db.refresh(user)

    response = user_to_user_response(user)

    return response


def change_user_admin_status(db: Session, id: int, user_admin_status: user_dtos.UserAdminStatus, request: Request) -> user_dtos.UserResponse:

    current_user = get_current_user(db, request)

    if not current_user.is_staff:
        raise ForbiddenException(current_user.email)

    user = db.query(models.User).filter(models.User.id == id).first()

    if user.is_staff:
        raise BadRequestException("Cannot modify admin status of super admin user")

    user.is_admin = user_admin_status.is_admin

    db.commit()
    db.refresh(user)

    response = user_to_user_response(user)

    return response


def change_user_avatar(db: Session, user_avatar: user_dtos.UserAvatar, request: Request) -> user_dtos.UserResponse:

    current_user = get_current_user(db, request)

    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    user.avatar = user_avatar.avatar

    db.commit()
    db.refresh(user)

    response = user_to_user_response(user)

    return response


def update_user(db: Session, id: int, request: Request, user_data: user_dtos.UserUpdate) -> user_dtos.UserResponse:

    username = get_username_from_token(request)

    password_hash, password_salt = utils.generate_hash_and_salt(user_data.password)

    user = db.query(models.User).filter(models.User.id == id).first()

    if user.is_staff:
        raise BadRequestException("Cannot modify super admin user")

    if user.username != username:
        raise ForbiddenException(username)

    user_data_username = user_data.email if user_data.email else user_data.phone_number

    if get_user_by_username(db, user_data_username) and user.username != user_data_username:
        raise BadRequestException(f"Cannot update username to '{user_data_username}'. User with username: '{user_data_username}' already exists")

    user.username = user_data_username
    user.email = user_data.email
    user.fname = user_data.first_name
    user.lname = user_data.last_name
    user.password_hash = password_hash
    user.password_salt = password_salt

    db.commit()
    db.refresh(user)

    response = user_to_user_response(user)

    return response


def get_users(db: Session, request: Request) -> List[user_dtos.UserResponse]:

    response = []

    current_user = get_current_user(db, request)

    if not current_user.is_admin:
        raise ForbiddenException(current_user.username)

    users = db.query(models.User).all()

    for user in users:
        response.append(user_to_user_response(user))

    return response


def get_user(db: Session, id: int, request: Request) -> user_dtos.UserResponse:

    current_user = get_current_user(db, request)
    user = get_user_by_id(db, id)

    if not user:
        raise NotFoundException(message=f"User with id: {id} does not exist")

    if not current_user.is_admin and current_user.username != user.username:
        raise ForbiddenException(current_user.email)

    return user


def forgot_password(db: Session, user: user_dtos.UserResponse) -> None:

    password_reset = models.PasswordReset(
        reset_code=utils.generate_reset_code(),
        expiry=RESET_CODE_EXPIRE_MINUTES
    )
    password_reset.user_id = user.id

    db.add(password_reset)
    db.commit()
    db.refresh(password_reset)

    payload = {
        "reset_code": password_reset.reset_code
    }

    email_service.send_email(user.email, FORGOT_PASSWORD_TEMPLATE, payload)


def reset_password(db: Session, reset_password_data: user_dtos.ResetPassword) -> user_dtos.UserResponse:

    password_reset = get_password_reset_by_reset_code(db, reset_password_data.reset_code)

    if not password_reset:
        raise BadRequestException("Invalid reset code")

    expiry = password_reset.created_on + timedelta(minutes=password_reset.expiry)
    if datetime.utcnow() > expiry:
        raise BadRequestException("Reset code has expired, please try again")

    password_hash, password_salt = utils.generate_hash_and_salt(reset_password_data.password)

    user = password_reset.user
    user.password_hash = password_hash
    user.password_salt = password_salt

    db.commit()
    db.refresh(user)

    response = user_to_user_response(user)

    return response


def get_current_user(db: Session, request: Request) -> user_dtos.UserResponse:

    username = get_username_from_token(request)
    user = get_user_by_username(db, username)

    return user


def get_user_by_username(db: Session, username: str) -> user_dtos.UserResponse:

    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        return None

    response = user_to_user_response(user)

    return response


def get_user_by_id(db: Session, id: int) -> user_dtos.UserResponse:

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        return None

    response = user_to_user_response(user)

    return response


def get_username_from_token(request: Request) -> EmailStr:

    token = request.headers.get("Authorization").split(" ")[1]
    payload = jwt_service.decode_jwt(token)
    username = payload.get("sub")

    return username


def get_password_reset_by_reset_code(db: Session, reset_code: str) -> models.PasswordReset:
    password_reset = db.query(models.PasswordReset).filter(models.PasswordReset.reset_code == reset_code).first()
    return password_reset
