from typing import Optional
from pydantic import BaseModel


class GameResponse(BaseModel):
    id: int
    score: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: Optional[int]


class GameCreateRequest(BaseModel):
    score: int
