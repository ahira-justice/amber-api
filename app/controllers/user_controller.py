from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm.session import Session
from typing import List

from app.domain.constants import USERS_URL
from app.domain.database import get_db
from app.auth.bearer import BearerAuth
from app.dtos import user_dtos
from app.dtos import error
from app.services import user_service


controller = APIRouter(
    prefix=USERS_URL,
    tags=["Users"]
)


@controller.post(
    path="",
    status_code=200,
    responses={
        200: {
            "model": user_dtos.UserResponse
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


@controller.get(
    path="",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": List[user_dtos.UserResponse]
        },
        401: {
            "model": error.ErrorResponse
        },
        403: {
            "model": error.ErrorResponse
        }
    }
)
async def get_all(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get users"""

    users = user_service.get_users(db, request)
    return users


@controller.get(
    path="/me",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": user_dtos.UserResponse
        },
        401: {
            "model": error.ErrorResponse
        },
        422: {
            "model": error.ValidationErrorResponse
        }
    }
)
async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get current user"""

    user = user_service.get_current_user(db, request)
    return user


@controller.put(
    path="/avatar",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": user_dtos.UserResponse
        },
        401: {
            "model": error.ErrorResponse
        },
        422: {
            "model": error.ValidationErrorResponse
        }
    }
)
async def set_user_avatar(
    user_avatar: user_dtos.UserAvatar,
    request: Request,
    db: Session = Depends(get_db)
):
    """Update user avatar"""

    updated_user = user_service.change_user_avatar(db, user_avatar, request)
    return updated_user


@controller.get(
    path="/{id}",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": user_dtos.UserResponse
        },
        401: {
            "model": error.ErrorResponse
        },
        403: {
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
    """Get user by id"""

    user = user_service.get_user(db, id, request)
    return user


@controller.put(
    path="/{id}",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": user_dtos.UserResponse
        },
        400: {
            "model": error.ErrorResponse
        },
        401: {
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

    return user_service.update_user(db, id, request, user_data)


@controller.put(
    path="/{id}/adminstatus",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": user_dtos.UserResponse
        },
        400: {
            "model": error.ErrorResponse
        },
        401: {
            "model": error.ErrorResponse
        },
        403: {
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

    return user_service.change_user_admin_status(db, id, user_admin_status, request)
