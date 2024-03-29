from alembic.config import Config
from alembic import command
from sqlalchemy.orm.session import Session

from app.domain.config import ADMIN_EMAIL, ADMIN_FIRST_NAME, ADMIN_LAST_NAME, ADMIN_PASSWORD
from app.domain.database import SessionLocal
from app.data.models import User
from loguru import logger
from app.services import user_service


def migrate_database(script_location: str, alembic_ini_location: str, dsn: str) -> None:

    logger.info(f"Running DB migrations in {script_location} on {dsn}")

    cfg = Config(alembic_ini_location)
    cfg.attributes['configure_logger'] = False

    command.upgrade(cfg, "head")

    seed()


def seed():
    logger.info("Seeding database...")

    db = SessionLocal()

    seed_super_admin(db)

    db.close()

    logger.info("Finished seeding database")


def seed_super_admin(db: Session):
    admin_user = db.query(User).filter(User.email == ADMIN_EMAIL).first()

    if not admin_user:
        admin_user = user_service.seed_user(db, ADMIN_EMAIL, ADMIN_FIRST_NAME, ADMIN_LAST_NAME, ADMIN_PASSWORD)
        user_service.set_super_admin(db, admin_user.id)
        logger.info(f"Created admin user; id: '{admin_user.id}', email: '{admin_user.email}'")
