from fastapi import Request
from pydantic import EmailStr
from sqlalchemy.orm.session import Session
from typing import List

from app.data import models
from app.dtos import auth_dtos, user_dtos
from app.commonhelper import utils
from app.exceptions.app_exceptions import BadRequestException, ForbiddenException, NotFoundException
from app.mappings.auth_mappings import external_login_to_user
from app.mappings.user_mappings import user_create_to_user, user_to_user_response
from app.services import auth_service


def create_user(db: Session, user_data: user_dtos.UserCreate) -> user_dtos.UserResponse:

    user = user_create_to_user(user_data)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user_to_user_response(user)


def create_social_user(db: Session, external_login_data: auth_dtos.ExternalLogin) -> user_dtos.UserResponse:

    user = external_login_to_user(external_login_data)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user_to_user_response(user)


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

    return user_to_user_response(user)


def change_user_admin_status(db: Session, id: int, user_admin_status: user_dtos.UserAdminStatus, request: Request) -> user_dtos.UserResponse:

    current_user = get_current_user(db, request)

    if not current_user.is_staff:
        raise ForbiddenException(current_user.email)

    user = get_user_by_id(db, id)

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

    return user_to_user_response(user)


def update_user(db: Session, id: int, request: Request, user_data: user_dtos.UserUpdate) -> user_dtos.UserResponse:

    username = get_username_from_token(request)

    password_hash, password_salt = utils.generate_hash_and_salt(user_data.password)

    user = get_user_by_id(db, id)

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
    user.instagram = user_data.instagram
    user.password_hash = password_hash
    user.password_salt = password_salt

    db.commit()
    db.refresh(user)

    return user_to_user_response(user)


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

    if not current_user.is_admin and current_user.username != user.username:
        raise ForbiddenException(current_user.email)

    return user_to_user_response(user)


def get_current_user(db: Session, request: Request) -> user_dtos.UserResponse:

    username = get_username_from_token(request)
    user = get_user_by_username(db, username)

    return user_to_user_response(user)


def get_user_by_username(db: Session, username: str) -> models.User:

    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        raise NotFoundException(message=f"User with username: {username} does not exist")

    return user


def get_user_by_id(db: Session, id: int) -> models.User:

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise NotFoundException(message=f"User with id: {id} does not exist")

    return user


def get_username_from_token(request: Request) -> EmailStr:

    token = request.headers.get("Authorization").split(" ")[1]
    payload = auth_service.decode_jwt(token)
    return payload.get("sub")
