import string
from faker import Faker
from sqlalchemy.orm.session import Session

from app.commonhelper import utils
from app.data.models import Game, User, UserToken
from app.domain.config import USER_TOKEN_RESET_PASSWORD_EXPIRE_MINUTES, USER_TOKEN_RESET_PASSWORD_LENGTH

fake = Faker()


def create_user(db: Session, password) -> User:
    password_hash, password_salt = utils.generate_hash_and_salt(password)

    user = User(
        username=fake.email(),
        email=fake.email(),
        fname=fake.first_name(),
        lname=fake.last_name(),
        password_hash=password_hash,
        password_salt=password_salt
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return user


def create_game(db: Session) -> Game:

    user = create_user(db, fake.password())

    game = Game(
        score=100,
        user_id=user.id
    )

    db.add(game)
    db.commit()
    db.refresh(game)
    db.close()

    return game


def create_user_token(db: Session) -> UserToken:

    user = create_user(db, fake.password())

    user_token = UserToken(
        token=utils.generate_code(USER_TOKEN_RESET_PASSWORD_LENGTH, string.ascii_letters),
        expiry=USER_TOKEN_RESET_PASSWORD_EXPIRE_MINUTES,
        user_id=user.id
    )

    db.add(user_token)
    db.commit()
    db.refresh(user_token)
    db.close()

    return user_token
