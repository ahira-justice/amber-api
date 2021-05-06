import hashlib
import os
import uuid

from typing import Tuple


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
