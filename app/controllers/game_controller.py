from fastapi import APIRouter, Depends, Request

from app.domain.constants import *


controller = APIRouter(
    prefix=GAMES_URL,
    tags=["Games"]
)
