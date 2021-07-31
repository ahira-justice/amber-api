from app.domain.database import SessionLocal
from app.data import models


def is_not_null(value) -> bool:
    if value:
        return True

    return False


def email_is_unique(email) -> bool:
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.email == email).first()
    db.close()

    if user:
        return False

    return True

def instagram_is_unique(instagram) -> bool:
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.instagram == instagram).first()
    db.close()

    if user:
        return False

    return True