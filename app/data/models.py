from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, LargeBinary
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

    lname = Column(String, nullable=False)
    fname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(LargeBinary, nullable=True)
    password_salt = Column(LargeBinary, nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    passwordresets = relationship("PasswordReset", back_populates="user", cascade="all, delete-orphan")


class PasswordReset(BaseEntity):

    __tablename__ = "passwordresets"

    reset_code = Column(String, nullable=False, index=True)
    expiry = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="passwordresets")
