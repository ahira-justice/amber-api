from typing import Optional
from pydantic import BaseModel


class GameResponse(BaseModel):
    id: int
    score: int
    username: str
    first_name: str
    last_name: str
    avatar: Optional[int]


class GameCreate(BaseModel):
    score: int
