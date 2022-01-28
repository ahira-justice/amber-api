from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.domain.constants import AUTH_URL
from app.domain.database import get_db
from app.dtos.auth_dtos import Token, ExternalLogin, ResetPassword, ForgotPassword, Login
from app.dtos.user_dtos import UserResponse 
from app.dtos.error_dtos import ErrorResponse, ValidationErrorResponse
from app.services import auth_service

controller = APIRouter(
    prefix=AUTH_URL,
    tags=["Auth"]
)


@controller.post(
    path="/login",
    status_code=200,
    responses={
        200: {"model": Token},
        401: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse}
    }
)
async def get_access_token(
    login_data: Login,
    db: Session = Depends(get_db)
):
    """Generate access token for valid credentials"""

    return auth_service.get_access_token(db, login_data)


@controller.post(
    path="/external-login",
    status_code=200,
    responses={
        200: {"model": Token},
        422: {"model": ValidationErrorResponse}
    }
)
async def get_access_token_for_external_login(
    external_login_data: ExternalLogin,
    db: Session = Depends(get_db)
):
    """Generate access token for valid credentials for social login"""

    return auth_service.get_access_token_for_external_login(db, external_login_data)


@controller.post(
    path="/forgot-password",
    status_code=204,
    responses={
        204: {},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse}
    }
)
async def forgot_password(
    forgot_password_data: ForgotPassword,
    db: Session = Depends(get_db)
):
    """Generate password reset link"""

    auth_service.forgot_password(db, forgot_password_data)


@controller.post(
    path="/reset-password",
    status_code=200,
    responses={
        200: {"model": UserResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse}
    }
)
async def reset_password(
    reset_password_data: ResetPassword,
    db: Session = Depends(get_db)
):
    """Reset user password"""

    return auth_service.reset_password(db, reset_password_data)
