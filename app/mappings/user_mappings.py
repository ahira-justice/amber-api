from app.data import models
from app.dtos import user_dtos
from app.commonhelper import utils


def user_to_user_response(user: models.User) -> user_dtos.UserResponse:

    result = user_dtos.UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        first_name=user.fname,
        last_name=user.lname,
        state=user.state,
        avatar=user.avatar,
        is_admin=user.is_admin,
        is_staff=user.is_staff
    )

    return result


def user_create_to_user(user_create: user_dtos.UserCreate) -> models.User:

    password_hash, password_salt = utils.generate_hash_and_salt(user_create.password)

    result = models.User(
        username=user_create.email,
        email=user_create.email,
        phone_number=user_create.phone_number,
        fname=user_create.first_name,
        lname=user_create.last_name,
        state=user_create.state,
        password_hash=password_hash,
        password_salt=password_salt
    )

    return result


def external_login_to_user(external_login: user_dtos.ExternalLogin) -> models.User:

    username = external_login.email if external_login.email else external_login.phone_number

    result = models.User(
        username=username,
        email=external_login.email,
        phone_number=external_login.phone_number,
        fname=external_login.first_name,
        lname=external_login.last_name
    )

    return result


def login_to_create_token(login: user_dtos.Login) -> user_dtos.CreateToken:

    result = user_dtos.CreateToken(
        username=login.username,
        expires=login.expires
    )

    return result


def external_login_to_create_token(external_login: user_dtos.ExternalLogin) -> user_dtos.CreateToken:

    username = external_login.email if external_login.email else external_login.phone_number

    result = user_dtos.CreateToken(
        username=username,
        expires=external_login.expires
    )

    return result
