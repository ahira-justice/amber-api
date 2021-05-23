from sqlalchemy.orm.session import Session

from app.commonhelper import utils
from app.data import models
from app.domain.config import *


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


def create_password_reset(db: Session) -> models.PasswordReset:

    user = create_user(db)

    password_reset = models.PasswordReset(
        reset_code=utils.generate_reset_code(),
        expiry=RESET_CODE_EXPIRE_MINUTES,
        user_id=user.id
    )

    db.add(password_reset)
    db.commit()
    db.refresh(password_reset)
    db.close()

    return password_reset
