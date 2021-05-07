from pydantic import BaseModel


class GameResponse(BaseModel):
    id: int
    score: int
    first_name: str
    last_name: str


class GameCreate(BaseModel):
    score: int
