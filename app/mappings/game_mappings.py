from app.data.models import Game
from app.dtos.game_dtos import GameCreate, GameResponse


def game_to_game_response(game: Game) -> GameResponse:

    result = GameResponse(
        id=game.id,
        score=game.score,
        username=game.user.username,
        first_name=game.user.fname,
        last_name=game.user.lname,
        instagram=game.user.instagram,
        avatar=game.user.avatar
    )

    return result


def game_create_to_game(game_create: GameCreate) -> Game:

    result = Game(
        score=game_create.score
    )

    return result
