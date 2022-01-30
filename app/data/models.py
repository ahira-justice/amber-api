from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

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

    lname = Column(String, nullable=True)
    fname = Column(String, nullable=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True, index=True)
    phone_number = Column(String, unique=True, nullable=True, index=True)
    password_hash = Column(LargeBinary, nullable=True)
    password_salt = Column(LargeBinary, nullable=True)
    avatar = Column(Integer, nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    games = relationship("Game", back_populates="user", cascade="all, delete-orphan")


class UserToken(BaseEntity):

    __tablename__ = "user_tokens"

    token = Column(String, nullable=False, index=True)
    token_type = Column(String, nullable=False)
    expiry = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class Game(BaseEntity):

    __tablename__ = "games"

    score = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="games")
