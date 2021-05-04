from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm.session import Session

from app.domain.config import *
from app.domain.constants import *
from app.domain.database import get_db
from app.auth.bearer import BearerAuth
from app.dtos import user_dtos
from app.dtos import error
from app.exceptions.app_exceptions import NotFoundException, UnauthorizedRequestException
from app.services import auth_service, jwt_service, user_service


controller = APIRouter(
    prefix=USERS_URL,
    tags=["Users"]
)


@controller.post(
    path="",
    responses={
        200: {
            "model": user_dtos.UserResponse
        },
        400: {
            "model": error.ErrorResponse
        },
        422: {
            "model": error.ValidationErrorResponse
        }
    }
)
async def register(
    user_data: user_dtos.UserCreate,
    db: Session = Depends(get_db)
):
    """Create new user"""

    new_user = user_service.create_user(db, user_data)
    return new_user


@controller.post(
    path="/token",
    responses={
        200: {
            "model": user_dtos.Token
        },
        400: {
            "model": error.ErrorResponse
        },
        422: {
            "model": error.ValidationErrorResponse
        }
    }
)
async def token(
    login_data: user_dtos.Login,
    db: Session = Depends(get_db)
):
    """Generate access token for valid credentials"""

    if not auth_service.authenticate_user(db, login_data.email, login_data.password):
        raise UnauthorizedRequestException("Incorrect email or password")

    token = jwt_service.create_access_token(login_data)

    return token


@controller.get(
    path="/{id}",
    dependencies=[Depends(BearerAuth())],
    responses={
        200: {
            "model": user_dtos.UserResponse
        },
        400: {
            "model": error.ErrorResponse
        },
        404: {
            "model": error.ErrorResponse
        },
        422: {
            "model": error.ValidationErrorResponse
        }
    }
)
async def get(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Get user"""

    user = user_service.get_user(db, id, request)

    return user


@controller.put(
    path="/{id}",
    dependencies=[Depends(BearerAuth())],
    responses={
        200: {
            "model": user_dtos.UserResponse
        },
        400: {
            "model": error.ErrorResponse
        },
        404: {
            "model": error.ErrorResponse
        },
        422: {
            "model": error.ValidationErrorResponse
        }
    }
)
async def update(
    id: int,
    user_data: user_dtos.UserUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Update user"""

    user = user_service.get_user_by_id(db, id)

    if not user:
        raise NotFoundException(f"User with id: {id} does not exist")

    updated_user = user_service.update_user(db, id, request, user_data)
    return updated_user


@controller.put(
    path="/{id}/adminstatus",
    dependencies=[Depends(BearerAuth())],
    responses={
        200: {
            "model": user_dtos.UserResponse
        },
        400: {
            "model": error.ErrorResponse
        },
        404: {
            "model": error.ErrorResponse
        },
        422: {
            "model": error.ValidationErrorResponse
        }
    }
)
async def change_admin_status(
    id: int,
    user_admin_status: user_dtos.UserAdminStatus,
    request: Request,
    db: Session = Depends(get_db)
):
    """Update user admin status"""

    user = user_service.get_user_by_id(db, id)

    if not user:
        raise NotFoundException(message=f"User with id: {id} does not exist")

    updated_user = user_service.change_user_admin_status(db, id, user_admin_status, request)
    return updated_user
