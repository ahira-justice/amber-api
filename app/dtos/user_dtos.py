from typing import Optional
from pydantic import BaseModel, EmailStr, validator

from app.validators import user_validator


class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr]
    phone_number: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: Optional[int]
    is_admin: bool = False
    is_staff: bool = False


class UserAdminStatusRequest(BaseModel):
    is_admin: bool = False


class UserAvatarRequest(BaseModel):
    avatar: int


class UserCreateRequest(BaseModel):
    email: EmailStr
    phone_number: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    password: str

    @validator("email")
    def email_is_not_null(cls, email):

        if not user_validator.is_not_null(email):
            raise ValueError("User email cannot be null")

        return email

    @validator("email")
    def email_is_unique(cls, email):

        if not user_validator.email_is_unique(email):
            raise ValueError(f"User with email: '{email}' already registered")

        return email

    @validator("password")
    def password_is_not_null(cls, password):

        if not user_validator.is_not_null(password):
            raise ValueError("User password cannot be null")

        return password


class UserUpdateRequest(BaseModel):
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    password: str

    @validator("email")
    def email_is_not_null(cls, email):

        if not user_validator.is_not_null(email):
            raise ValueError("User email cannot be null")

        return email

    @validator("phone_number")
    def phone_number_is_not_null(cls, phone_number):

        if not user_validator.is_not_null(phone_number):
            raise ValueError("User phone number cannot be null")

        return phone_number

    @validator("last_name")
    def last_name_is_not_null(cls, last_name):

        if not user_validator.is_not_null(last_name):
            raise ValueError("User last name cannot be null")

        return last_name

    @validator("first_name")
    def first_name_is_not_null(cls, first_name):

        if not user_validator.is_not_null(first_name):
            raise ValueError("User first name cannot be null")

        return first_name
