from typing import Optional
from pydantic import BaseModel, EmailStr, validator, root_validator

from app.domain.config import *
from app.validators import user_validator


class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr]
    phone_number: Optional[str]
    first_name: str
    last_name: str
    state: Optional[str]
    avatar: Optional[int]
    is_admin: bool = False
    is_staff: bool = False


class UserAdminStatus(BaseModel):
    is_admin: bool = False


class UserAvatar(BaseModel):
    avatar: int


class UserCreate(BaseModel):
    email: EmailStr
    phone_number: Optional[str]
    first_name: str
    last_name: str
    state: Optional[str]
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

    @validator("state")
    def state_is_not_null(cls, state):

        if not user_validator.is_not_null(state):
            raise ValueError("User state cannot be null")

        return state

    @validator("password")
    def password_is_not_null(cls, password):

        if not user_validator.is_not_null(password):
            raise ValueError("User password cannot be null")

        return password


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
            raise ValueError("User last name cannot be null")

        return last_name

    @validator("first_name")
    def first_name_is_not_null(cls, first_name):

        if not user_validator.is_not_null(first_name):
            raise ValueError("User first name cannot be null")

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
