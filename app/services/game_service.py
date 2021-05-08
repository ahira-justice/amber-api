from datetime import datetime, timedelta
from fastapi import Request
from sqlalchemy import desc
from sqlalchemy.orm.session import Session
from typing import List

from app.dtos import game_dtos
from app.exceptions.app_exceptions import ForbiddenException, NotFoundException
from app.mappings.game_mappings import *
from app.services import user_service


def create_game(db: Session, request: Request, game_data: game_dtos.GameCreate) -> game_dtos.GameResponse:
    user = user_service.get_current_user(db, request)
    game = game_create_to_game(game_data)
    game.user_id = user.id

    db.add(game)
    db.commit()
    db.refresh(game)

    response = game_to_game_response(game)

    return response


def get_games(db: Session, request: Request) -> List[game_dtos.GameResponse]:

    response = []

    current_user = user_service.get_current_user(db, request)

    games = db.query(models.Game).filter(models.Game.user_id == current_user.id).all()

    if current_user.is_admin:
        games = db.query(models.Game).all()

    for game in games:
        response.append(game_to_game_response(game))

    return response


def get_game(db: Session, id: int, request: Request) -> game_dtos.GameResponse:

    current_user = user_service.get_current_user(db, request)
    game = get_game_by_id(db, id)

    if not game:
        raise NotFoundException(f"Game with id: {id} does not exist")

    if not current_user.is_admin and current_user.email != game.email:
        raise ForbiddenException(current_user.email)

    return game


def get_leaderboard(db: Session) -> List[game_dtos.GameResponse]:

    response = []
    today = datetime.today().date()
    weekstart = today + timedelta(days=-today.weekday())

    games = db.query(models.Game)

    games = games.filter(models.Game.created_on >= weekstart)
    games = games.order_by(desc(models.Game.score),models.Game.created_on).all()

    for game in games:
        response.append(game_to_game_response(game))

    return response


def get_game_by_id(db: Session, id: int) -> game_dtos.GameResponse:

    game = db.query(models.Game).filter(models.Game.id == id).first()

    if not game:
        return None

    response = game_to_game_response(game)

    return response
