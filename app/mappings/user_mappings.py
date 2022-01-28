from app.data.models import User
from app.dtos.user_dtos import UserResponse, UserCreate
from app.commonhelper import utils


def user_to_user_response(user: User) -> UserResponse:

    result = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        first_name=user.fname,
        last_name=user.lname,
        instagram=user.instagram,
        state=user.state,
        avatar=user.avatar,
        is_admin=user.is_admin,
        is_staff=user.is_staff
    )

    return result


def user_create_to_user(user_create: UserCreate) -> User:

    password_hash, password_salt = utils.generate_hash_and_salt(user_create.password)

    result = User(
        username=user_create.email,
        email=user_create.email,
        phone_number=user_create.phone_number,
        fname=user_create.first_name,
        lname=user_create.last_name,
        instagram=user_create.instagram,
        state=user_create.state,
        password_hash=password_hash,
        password_salt=password_salt
    )

    return result
