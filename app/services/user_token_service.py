from datetime import datetime, timedelta
from sqlalchemy.orm.session import Session

from app.commonhelper import utils
from app.data.models import UserToken
from app.data.enums import UserTokenType
from app.dtos.user_token_dtos import VerifyUserTokenRequest
from app.exceptions.app_exceptions import BadRequestException
from app.services import user_service


def generate_token(db: Session, length: int, keyspace: str, expiry: int, token_type: UserTokenType, user_id: int) -> UserToken:

    user = user_service.get_user_by_id(db, user_id)

    validate_expiry(expiry)
    delete_old_token_if_exists(db, user.id, token_type)

    user_token = UserToken(
        token=utils.generate_code(length, keyspace),
        token_type=token_type.name,
        expiry=expiry
    )

    user_token.user_id = user.id

    db.add(user_token)
    db.commit()
    db.refresh(user_token)

    return user_token


def use_token(db: Session, user_id: int, token: str, token_type: UserTokenType):

    if not validate_token(db, user_id, token, token_type):
        raise BadRequestException("Invalid user token")
    
    db.query(UserToken).filter(UserToken.user_id == user_id, UserToken.token_type == token_type.name).delete()
    db.commit()


def verify_user_token(db: Session, request: VerifyUserTokenRequest) -> bool:

    user = user_service.get_user_by_username(request.username)

    if request.token_type not in UserTokenType.__members__:
        raise BadRequestException("Invalid token type")

    return validate_token(db, user.id, request.token, UserTokenType[request.token_type])


def validate_token(db: Session, user_id: int, token: str, token_type: UserTokenType) -> bool:

    user_token = db.query(UserToken).filter(UserToken.user_id == user_id, UserToken.token_type == token_type.name).first()

    if not user_token:
        raise BadRequestException(f"User token for token type: {token_type.name} does not exist for given user")

    expiry = user_token.created_on + timedelta(minutes=user_token.expiry)

    if datetime.utcnow() > expiry:
        raise BadRequestException("User token has expired, please try again")
    
    return user_token.token == token


def validate_expiry(expiry: int):
    if expiry <= 0:
        raise BadRequestException("Expiry in minutes must be greater than 0")


def delete_old_token_if_exists(db: Session, user_id: int, token_type: UserTokenType):
    db.query(UserToken).filter(UserToken.user_id == user_id, UserToken.token_type == token_type.name).delete()
    db.commit()
