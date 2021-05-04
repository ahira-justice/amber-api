from fastapi import Request
from pydantic import EmailStr
from sqlalchemy.orm.session import Session

from app.data import models
from app.dtos import user_dtos
from app.commonhelper import utils
from app.exceptions.app_exceptions import BadRequestException, ForbiddenException
from app.mappings.user_mappings import *
from app.services import jwt_service


def create_user(db: Session, user_data: user_dtos.UserCreate) -> user_dtos.UserResponse:

    user = user_create_to_user(user_data)

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

    token = request.headers.get("Authorization").split(" ")[1]
    payload = jwt_service.decode_jwt(token)
    email = payload.get("sub")

    requesting_user = db.query(models.User).filter(models.User.email == email).first()

    if not requesting_user.is_staff:
        raise ForbiddenException(requesting_user.email)

    user = db.query(models.User).filter(models.User.id == id).first()

    if user.is_staff:
        raise BadRequestException("Cannot modify admin status of super admin user")

    user.is_admin = user_admin_status.is_admin

    db.commit()
    db.refresh(user)

    response = user_to_user_response(user)

    return response


def update_user(db: Session, id: int, request: Request, user_data: user_dtos.UserUpdate) -> user_dtos.UserResponse:

    token = request.headers.get("Authorization").split(" ")[1]
    payload = jwt_service.decode_jwt(token)
    email = payload.get("sub")

    password_hash, password_salt = utils.generate_hash_and_salt(user_data.password)

    user = db.query(models.User).filter(models.User.id == id).first()

    if user.is_staff:
        raise BadRequestException("Cannot modify super admin user")

    if user.email != email:
        raise ForbiddenException(email)

    if db.query(models.User).filter(models.User.email == user_data.email).first() and user.email != user_data.email:
        raise BadRequestException(f"Cannot update email to '{user_data.email}'. User with email: '{user_data.email}' already exists")

    user.email = user_data.email
    user.fname = user_data.first_name
    user.lname = user_data.last_name
    user.password_hash = password_hash
    user.password_salt = password_salt

    db.commit()
    db.refresh(user)

    response = user_to_user_response(user)

    return response


def get_user_by_email(db: Session, email: EmailStr) -> user_dtos.UserResponse:

    user = db.query(models.User).filter(models.User.email == email).first()

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
