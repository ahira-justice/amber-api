import hashlib
import os
import uuid

from typing import List, Tuple

from app.data import models


def generate_hash_and_salt(password: str) -> Tuple[bytes]:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000,
        dklen=128
    )

    return key, salt


def generate_reset_code() -> int:
    return uuid.uuid4()


def remove_duplicates(games: List[models.Game]) -> List[models.Game]:
    user_ids = [].append(games[0].user_id)
    result = games.copy()

    for index in range(1, len(games)):
        game = games[index]

        if game.user_id not in user_ids:
            user_ids.append(game.user_id)

        if game.user_id in user_ids:
            result.pop(index)

    return result
