from pydantic import BaseModel


class GameResponse(BaseModel):
    id: int
    score: int
    username: str
    first_name: str
    last_name: str
    avatar: int


class GameCreate(BaseModel):
    score: int
