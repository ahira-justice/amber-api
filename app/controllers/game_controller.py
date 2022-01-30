from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm.session import Session
from typing import List

from app.auth.bearer import BearerAuth
from app.domain.constants import GAMES_URL
from app.domain.database import get_db
from app.dtos.error_dtos import ErrorResponse, ValidationErrorResponse
from app.dtos.game_dtos import GameResponse, GameCreateRequest
from app.services import game_service

controller = APIRouter(
    prefix=GAMES_URL,
    tags=["Games"]
)


@controller.post(
    path="",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {"model": GameResponse},
        401: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse}
    }
)
async def create_game(
        game_data: GameCreateRequest,
        request: Request,
        db: Session = Depends(get_db)
):
    """Create new game"""

    return game_service.create_game(db, request, game_data)


@controller.get(
    path="",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {"model": List[GameResponse]},
        401: {"model": ErrorResponse}
    }
)
async def get_games(
        request: Request,
        db: Session = Depends(get_db)
):
    """Get games"""

    return game_service.get_games(db, request)


@controller.get(
    path="/daily-leaderboard",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {"model": List[GameResponse]},
        401: {"model": ErrorResponse}
    }
)
async def get_daily_leaderboard(
        db: Session = Depends(get_db)
):
    """Get daily leaderboard"""

    return game_service.get_daily_leaderboard(db)


@controller.get(
    path="/weekly-leaderboard",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {"model": List[GameResponse]},
        401: {"model": ErrorResponse}
    }
)
async def get_weekly_leaderboard(
        db: Session = Depends(get_db)
):
    """Get weekly leaderboard"""

    return game_service.get_weekly_leaderboard(db)


@controller.get(
    path="/all-time-leaderboard",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {"model": List[GameResponse]},
        401: {"model": ErrorResponse}
    }
)
async def get_all_time_leaderboard(
        db: Session = Depends(get_db)
):
    """Get all-time leaderboard"""

    return game_service.get_all_time_leaderboard(db)


@controller.get(
    path="/{id}",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {"model": GameResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse}
    }
)
async def get_game(
        id: int,
        request: Request,
        db: Session = Depends(get_db)
):
    """Get game"""

    return game_service.get_game(db, id, request)
