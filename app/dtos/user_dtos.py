from typing import Optional
from pydantic import BaseModel, EmailStr, validator

from app.domain.config import *
from app.validators import user_validator


class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr]
    phone_number: Optional[str]
    first_name: str
    last_name: str
    is_admin: bool = False
    is_staff: bool = False


class UserAdminStatus(BaseModel):
    is_admin: bool = False


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
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

    @validator("last_name")
    def last_name_is_not_null(cls, last_name):

        if not user_validator.is_not_null(last_name):
            raise ValueError("User last_name cannot be null")

        return last_name

    @validator("first_name")
    def first_name_is_not_null(cls, first_name):

        if not user_validator.is_not_null(first_name):
            raise ValueError("User first_name cannot be null")

        return first_name


class UserUpdate(BaseModel):
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
            raise ValueError("User last_name cannot be null")

        return last_name

    @validator("first_name")
    def first_name_is_not_null(cls, first_name):

        if not user_validator.is_not_null(first_name):
            raise ValueError("User first_name cannot be null")

        return first_name


class Login(BaseModel):
    username: str
    password: str
    expires: Optional[int] = ACCESS_TOKEN_EXPIRE_MINUTES


class CreateToken(BaseModel):
    username: str
    expires: Optional[int] = ACCESS_TOKEN_EXPIRE_MINUTES


class ExternalLogin(BaseModel):
    email: Optional[EmailStr]
    phone_number: Optional[str]
    first_name: str
    last_name: str
    expires: Optional[int] = ACCESS_TOKEN_EXPIRE_MINUTES

    @validator("email", "phone_number")
    def email_or_phone_number_is_not_null(cls, values):

        email, phone_number = values

        if not user_validator.is_not_null(email) or not user_validator.is_not_null(phone_number):
            raise ValueError("User email or phone number cannot be null")

        if user_validator.is_not_null(email) and user_validator.is_not_null(phone_number):
            raise ValueError("User email and phone number cannot both be set")

        return email or phone_number

    @validator("last_name")
    def last_name_is_not_null(cls, last_name):

        if not user_validator.is_not_null(last_name):
            raise ValueError("User last_name cannot be null")

        return last_name

    @validator("first_name")
    def first_name_is_not_null(cls, first_name):

        if not user_validator.is_not_null(first_name):
            raise ValueError("User first_name cannot be null")

        return first_name


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    password: str
    reset_code: str


class Password(BaseModel):
    password_hash: bytes
    password_salt: bytes


class Token(BaseModel):
    access_token: str
    token_type: str
