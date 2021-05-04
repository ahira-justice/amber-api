from app.data import models
from app.dtos import user_dtos
from app.commonhelper import utils


def user_to_user_response(user: models.User) -> user_dtos.UserResponse:
    result = user_dtos.UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.fname,
        last_name=user.lname,
        is_admin=user.is_admin
    )

    return result


def user_create_to_user(user_create: user_dtos.UserCreate) -> models.User:
    password_hash, password_salt = utils.generate_hash_and_salt(user_create.password)

    result = models.User(
        email=user_create.email,
        fname=user_create.first_name,
        lname=user_create.last_name,
        password_hash=password_hash,
        password_salt=password_salt
    )

    return result
