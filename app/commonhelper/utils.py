import hashlib
import os
import random

from typing import List, Tuple

from app.data import models


def generate_hash_and_salt(password: str) -> tuple[bytes, bytes]:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000,
        dklen=128
    )

    return key, salt


def generate_code(length: int, key_space: str) -> str:
    return ''.join((random.choice(key_space) for x in range(length)))


def remove_duplicates(games: List[models.Game]) -> List[models.Game]:
    result_dict = {}

    for game in games:
        if game.user_id not in result_dict.keys():
            result_dict[game.user_id] = game

    return list(result_dict.values())
