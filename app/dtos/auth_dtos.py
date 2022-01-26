from typing import Optional
from pydantic import BaseModel, EmailStr, validator, root_validator

from app.domain.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.validators import user_validator


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

    @root_validator()
    def email_or_phone_number_is_not_null(cls, values):
        email = values.get("email")
        phone_number = values.get("phone_number")

        if not user_validator.is_not_null(email) and not user_validator.is_not_null(phone_number):
            raise ValueError("User email and phone number cannot be null")

        if user_validator.is_not_null(email) and user_validator.is_not_null(phone_number):
            raise ValueError("User email and phone number cannot both be set")

        return values

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


class ForgotPassword(BaseModel):
    username: str


class ResetPassword(BaseModel):
    username: str
    password: str
    token: str


class Password(BaseModel):
    password_hash: bytes
    password_salt: bytes


class Token(BaseModel):
    access_token: str
    token_type: str
