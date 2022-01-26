import string
from sqlalchemy.orm.session import Session

from app.commonhelper import utils
from app.data import models
from app.domain.config import USER_TOKEN_RESET_PASSWORD_EXPIRE_MINUTES, USER_TOKEN_RESET_PASSWORD_LENGTH


def create_user(db: Session) -> models.User:

    password_hash, password_salt = utils.generate_hash_and_salt("password")

    user = models.User(
        username="user@example.com",
        email="user@example.com",
        fname="Test",
        lname="User",
        password_hash=password_hash,
        password_salt=password_salt
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return user


def create_game(db: Session) -> models.Game:

    user = create_user(db)

    game = models.Game(
        score=100,
        user_id=user.id
    )

    db.add(game)
    db.commit()
    db.refresh(game)
    db.close()

    return game


def create_user_token(db: Session) -> models.UserToken:

    user = create_user(db)

    user_token = models.UserToken(
        token=utils.generate_code(USER_TOKEN_RESET_PASSWORD_LENGTH, string.ascii_letters),
        expiry=USER_TOKEN_RESET_PASSWORD_EXPIRE_MINUTES,
        user_id=user.id
    )

    db.add(user_token)
    db.commit()
    db.refresh(user_token)
    db.close()

    return user_token
