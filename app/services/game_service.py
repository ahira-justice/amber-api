from fastapi import Request
from sqlalchemy.orm.session import Session
from typing import List

from app.dtos import game_dtos


def create_game(db: Session, game_data: game_dtos.GameCreate) -> game_dtos.GameResponse:
    pass


def get_games(db: Session, request: Request) -> List[game_dtos.GameResponse]:
    pass


def get_game(db: Session, id: int, request: Request):
    pass


def get_game_by_id(db: Session, id: int) -> game_dtos.GameResponse:
    pass
