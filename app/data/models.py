from sqlalchemy import Boolean, Column, DateTime, Integer, String, LargeBinary

from datetime import datetime

from app.domain.database import Base


class BaseEntity(Base):

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_on = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_on = Column(DateTime, default=None, onupdate=datetime.utcnow, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)


class User(BaseEntity):

    __tablename__ = "users"

    lname = Column(String, nullable=False)
    fname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(LargeBinary, nullable=True)
    password_salt = Column(LargeBinary, nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_staff = Column(Boolean, nullable=False, default=False)
