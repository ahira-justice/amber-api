from app.commonhelper import utils
from datetime import datetime, timedelta
from fastapi import Request
from sqlalchemy import desc
from sqlalchemy.orm.session import Session
from typing import List

from app.data.models import Game
from app.domain.config import ALL_TIME_LEADERBOARD_LIMIT
from app.dtos.game_dtos import GameCreateRequest, GameResponse
from app.exceptions.app_exceptions import ForbiddenException, NotFoundException
from app.mappings.game_mappings import game_create_to_game, game_to_game_response
from app.services import user_service


def create_game(db: Session, request: Request, game_data: GameCreateRequest) -> GameResponse:
    user = user_service.get_current_user(db, request)
    game = game_create_to_game(game_data)
    game.user_id = user.id

    db.add(game)
    db.commit()
    db.refresh(game)

    response = game_to_game_response(game)

    return response


def get_games(db: Session, request: Request) -> List[GameResponse]:

    response = []

    current_user = user_service.get_current_user(db, request)

    games = db.query(Game).filter(Game.user_id == current_user.id).all()

    if current_user.is_admin:
        games = db.query(Game).all()

    for game in games:
        response.append(game_to_game_response(game))

    return response


def get_game(db: Session, id: int, request: Request) -> GameResponse:

    current_user = user_service.get_current_user(db, request)
    game = get_game_by_id(db, id)

    if not game:
        raise NotFoundException(message=f"Game with id: {id} does not exist")

    if not current_user.is_admin and current_user.username != game.user.username:
        raise ForbiddenException(current_user.username)

    return game_to_game_response(game)


def get_daily_leaderboard(db: Session) -> List[GameResponse]:

    today = datetime.today()

    return get_leaderboard(db, today)


def get_weekly_leaderboard(db: Session) -> List[GameResponse]:

    today = datetime.today()
    week_start = today + timedelta(days=-today.weekday())

    return get_leaderboard(db, week_start)


def get_all_time_leaderboard(db: Session) -> List[GameResponse]:

    response = []

    games = db.query(Game)

    games = games.order_by(desc(Game.score), Game.created_on).all()

    games = utils.remove_duplicates(games)

    games.sort(key=lambda x: x.created_on)
    games.sort(key=lambda x: x.score, reverse=True)

    games = games[:ALL_TIME_LEADERBOARD_LIMIT]

    for game in games:
        response.append(game_to_game_response(game))

    return response


def get_leaderboard(db: Session, limit: datetime) -> List[GameResponse]:
    response = []

    games = db.query(Game)

    games = games.filter(Game.created_on >= limit)
    games = games.order_by(desc(Game.score), Game.created_on).all()

    games = utils.remove_duplicates(games)

    games.sort(key=lambda x: x.created_on)
    games.sort(key=lambda x: x.score, reverse=True)

    for game in games:
        response.append(game_to_game_response(game))

    return response


def get_game_by_id(db: Session, id: int) -> Game:

    game = db.query(Game).filter(Game.id == id).first()

    if not game:
        raise NotFoundException(message=f"Game with id: {id} does not exist")

    return game
