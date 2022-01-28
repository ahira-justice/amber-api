from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm.session import Session
from typing import List

from app.domain.constants import USERS_URL
from app.domain.database import get_db
from app.auth.bearer import BearerAuth
from app.dtos.user_dtos import UserResponse, UserCreate, UserAvatar, UserUpdate, UserAdminStatus
from app.dtos.error_dtos import ErrorResponse, ValidationErrorResponse
from app.services import user_service


controller = APIRouter(
    prefix=USERS_URL,
    tags=["Users"]
)


@controller.post(
    path="",
    status_code=200,
    responses={
        200: {"model": UserResponse},
        422: {"model": ValidationErrorResponse}
    }
)
async def create_user(
        user_data: UserCreate,
        db: Session = Depends(get_db)
):
    """Create new user"""

    return user_service.create_user(db, user_data)


@controller.get(
    path="",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {"model": List[UserResponse]},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse}
    }
)
async def get_users(
        request: Request,
        db: Session = Depends(get_db)
):
    """Get users"""

    return user_service.get_users(db, request)


@controller.get(
    path="/me",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {"model": UserResponse},
        401: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse}
    }
)
async def get_current_user(
        request: Request,
        db: Session = Depends(get_db)
):
    """Get current user"""

    return user_service.get_current_user(db, request)


@controller.put(
    path="/avatar",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {"model": UserResponse},
        401: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse}
    }
)
async def set_user_avatar(
        user_avatar: UserAvatar,
        request: Request,
        db: Session = Depends(get_db)
):
    """Update user avatar"""

    return user_service.set_user_avatar(db, user_avatar, request)


@controller.get(
    path="/{id}",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {"model": UserResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse}
    }
)
async def get_user(
        id: int,
        request: Request,
        db: Session = Depends(get_db)
):
    """Get user by id"""

    return user_service.get_user(db, id, request)


@controller.put(
    path="/{id}",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {"model": UserResponse},
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse}
    }
)
async def update_user(
        id: int,
        user_data: UserUpdate,
        request: Request,
        db: Session = Depends(get_db)
):
    """Update user"""

    return user_service.update_user(db, id, request, user_data)


@controller.put(
    path="/{id}/admin-status",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {"model": UserResponse},
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse}
    }
)
async def change_admin_status(
        id: int,
        user_admin_status: UserAdminStatus,
        request: Request,
        db: Session = Depends(get_db)
):
    """Update user admin status"""

    return user_service.change_admin_status(db, id, user_admin_status, request)
