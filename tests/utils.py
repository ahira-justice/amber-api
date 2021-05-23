from sqlalchemy.orm.session import Session

from app.data import models
from app.domain.database import Base, SessionLocal, engine


def get_db() -> Session:
    db = SessionLocal()
    return db


def create_tables():
    Base.metadata.create_all(bind=engine)


def setup():
    print("\nCreating test database tables...\n")
    create_tables()


def clear_db_data(db: Session):
    db.query(models.User).delete()
    db.query(models.Game).delete()
    db.query(models.PasswordReset).delete()
    db.commit()

    db.close()
