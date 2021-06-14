from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm.session import Session
from typing import List

from app.auth.bearer import BearerAuth
from app.domain.constants import *
from app.domain.database import get_db
from app.dtos import error
from app.dtos import game_dtos
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
        200: {
            "model": game_dtos.GameResponse
        },
        401: {
            "model": error.ErrorResponse
        },
        422: {
            "model": error.ValidationErrorResponse
        }
    }
)
async def create(
    game_data: game_dtos.GameCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Create new game"""

    new_game = game_service.create_game(db, request, game_data)
    return new_game


@controller.get(
    path="",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": List[game_dtos.GameResponse]
        },
        401: {
            "model": error.ErrorResponse
        }
    }
)
async def get_all(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get games"""

    games = game_service.get_games(db, request)
    return games


@controller.get(
    path="/dailyleaderboard",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": List[game_dtos.GameResponse]
        },
        401: {
            "model": error.ErrorResponse
        }
    }
)
async def daily_leaderboard(
    db: Session = Depends(get_db)
):
    """Get weekly leaderboard"""

    daily_leaderboard = game_service.get_daily_leaderboard(db)
    return daily_leaderboard


@controller.get(
    path="/weeklyleaderboard",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": List[game_dtos.GameResponse]
        },
        401: {
            "model": error.ErrorResponse
        }
    }
)
async def weekly_leaderboard(
    db: Session = Depends(get_db)
):
    """Get weekly leaderboard"""

    weekly_leaderboard = game_service.get_weekly_leaderboard(db)
    return weekly_leaderboard


@controller.get(
    path="/alltimeleaderboard",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": List[game_dtos.GameResponse]
        },
        401: {
            "model": error.ErrorResponse
        }
    }
)
async def all_time_leaderboard(
    db: Session = Depends(get_db)
):
    """Get all-time leaderboard"""

    all_time_leaderboard = game_service.get_all_time_leaderboard(db)
    return all_time_leaderboard


@controller.get(
    path="/{id}",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": game_dtos.GameResponse
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
    """Get game"""

    game = game_service.get_game(db, id, request)
    return game
