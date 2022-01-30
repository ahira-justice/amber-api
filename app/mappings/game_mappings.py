from app.data.models import Game
from app.dtos.game_dtos import GameCreateRequest, GameResponse


def game_to_game_response(game: Game) -> GameResponse:

    result = GameResponse(
        id=game.id,
        score=game.score,
        username=game.user.username,
        first_name=game.user.fname,
        last_name=game.user.lname,
        avatar=game.user.avatar
    )

    return result


def game_create_to_game(game_create: GameCreateRequest) -> Game:

    result = Game(
        score=game_create.score
    )

    return result
