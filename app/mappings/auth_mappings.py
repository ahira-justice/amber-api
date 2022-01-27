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
