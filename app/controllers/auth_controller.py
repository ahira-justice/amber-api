from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.domain.constants import AUTH_URL
from app.domain.database import get_db
from app.dtos import auth_dtos, user_dtos
from app.dtos import error_dtos
from app.exceptions.app_exceptions import UnauthorizedRequestException
from app.mappings.auth_mappings import external_login_to_create_token, login_to_create_token
from app.services import auth_service, jwt_service, user_service


controller = APIRouter(
    prefix=AUTH_URL,
    tags=["Auth"]
)


@controller.post(
    path="/login",
    status_code=200,
    responses={
        200: {
            "model": auth_dtos.Token
        },
        401: {
            "model": error_dtos.ErrorResponse
        },
        422: {
            "model": error_dtos.ValidationErrorResponse
        }
    }
)
async def login(
    login_data: auth_dtos.Login,
    db: Session = Depends(get_db)
):
    """Generate access token for valid credentials"""

    if not auth_service.authenticate_user(db, login_data.username, login_data.password):
        raise UnauthorizedRequestException("Incorrect username or password")

    create_token_data = login_to_create_token(login_data)
    token = jwt_service.create_access_token(create_token_data)

    return token


@controller.post(
    path="/externallogin",
    status_code=200,
    responses={
        200: {
            "model": auth_dtos.Token
        },
        422: {
            "model": error_dtos.ValidationErrorResponse
        }
    }
)
async def external_login(
    external_login_data: auth_dtos.ExternalLogin,
    db: Session = Depends(get_db)
):
    """Generate access token for valid credentials for social login"""

    username = external_login_data.email if external_login_data.email else external_login_data.phone_number

    user = user_service.get_user_by_username(db, username)

    if not user:
        user_service.create_social_user(db, external_login_data)

    create_token_data = external_login_to_create_token(external_login_data)
    token = jwt_service.create_access_token(create_token_data)

    return token


@controller.post(
    path="/forgotpassword",
    status_code=204,
    responses={
        204: {},
        404: {
            "model": error_dtos.ErrorResponse
        },
        422: {
            "model": error_dtos.ValidationErrorResponse
        }
    }
)
async def forgot_password(
    forgot_password_data: auth_dtos.ForgotPassword,
    db: Session = Depends(get_db)
):
    """Generate password reset link"""
    auth_service.forgot_password(db, forgot_password_data)


@controller.post(
    path="/resetpassword",
    status_code=200,
    responses={
        200: {
            "model": user_dtos.UserResponse
        },
        404: {
            "model": error_dtos.ErrorResponse
        },
        422: {
            "model": error_dtos.ValidationErrorResponse
        }
    }
)
async def reset_password(
    reset_password_data: auth_dtos.ResetPassword,
    db: Session = Depends(get_db)
):
    """Reset user password"""
    return auth_service.reset_password(db, reset_password_data)
