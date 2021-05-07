from fastapi import Request
from sqlalchemy.orm.session import Session
from typing import List

from app.dtos import game_dtos
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
    pass


def get_game(db: Session, id: int, request: Request):
    pass


def get_game_by_id(db: Session, id: int) -> game_dtos.GameResponse:
    pass
