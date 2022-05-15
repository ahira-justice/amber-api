from sqlalchemy.orm.session import Session

from app.data.models import Base
from app.domain.database import SessionLocal, engine


def get_db() -> Session:
    db = SessionLocal()
    return db


def create_tables():
    Base.metadata.create_all(bind=engine)


def setup():
    print("\nCreating test database tables...\n")
    create_tables()
