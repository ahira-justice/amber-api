from sqlalchemy import Boolean, Column, Integer, String, LargeBinary

from app.domain.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    lname = Column(String, nullable=False)
    fname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(LargeBinary, nullable=True)
    password_salt = Column(LargeBinary, nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_staff = Column(Boolean, nullable=False, default=False)
