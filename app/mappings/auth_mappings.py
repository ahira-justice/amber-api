from app.data import models
from app.dtos import auth_dtos


def external_login_to_user(external_login: auth_dtos.ExternalLogin) -> models.User:

    username = external_login.email if external_login.email else external_login.phone_number

    result = models.User(
        username=username,
        email=external_login.email,
        phone_number=external_login.phone_number,
        fname=external_login.first_name,
        lname=external_login.last_name
    )

    return result


def login_to_create_token(login: auth_dtos.Login) -> auth_dtos.CreateToken:

    result = auth_dtos.CreateToken(
        username=login.username,
        expires=login.expires
    )

    return result


def external_login_to_create_token(external_login: auth_dtos.ExternalLogin) -> auth_dtos.CreateToken:

    username = external_login.email if external_login.email else external_login.phone_number

    result = auth_dtos.CreateToken(
        username=username,
        expires=external_login.expires
    )

    return result
