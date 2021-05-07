from app.data import models
from app.dtos import game_dtos


def game_to_game_response(game: models.Game) -> game_dtos.GameResponse:

    result = game_dtos.GameResponse(
        id=game.id,
        score=game.score,
        email=game.user.email,
        first_name=game.user.fname,
        last_name=game.user.lname
    )

    return result


def game_create_to_game(game_create: game_dtos.GameCreate) -> models.Game:

    result = models.Game(
        score=game_create.score
    )

    return result
