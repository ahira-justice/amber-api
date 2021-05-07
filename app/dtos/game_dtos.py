from pydantic import BaseModel, EmailStr


class GameResponse(BaseModel):
    id: int
    score: int
    email: EmailStr
    first_name: str
    last_name: str


class GameCreate(BaseModel):
    score: int
