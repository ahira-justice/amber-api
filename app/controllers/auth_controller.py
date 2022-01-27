from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.domain.constants import AUTH_URL
from app.domain.database import get_db
from app.dtos import auth_dtos, user_dtos
from app.dtos import error_dtos
from app.services import auth_service, user_service


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
async def get_access_token(
    login_data: auth_dtos.Login,
    db: Session = Depends(get_db)
):
    """Generate access token for valid credentials"""

    return auth_service.get_access_token(db, login_data)


@controller.post(
    path="/external-login",
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
async def get_access_token_for_external_login(
    external_login_data: auth_dtos.ExternalLogin,
    db: Session = Depends(get_db)
):
    """Generate access token for valid credentials for social login"""

    return auth_service.get_access_token_for_external_login(db, external_login_data)


@controller.post(
    path="/forgot-password",
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
    path="/reset-password",
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
