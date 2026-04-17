from datetime import datetime

from pydantic import BaseModel, EmailStr


# shared data
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool
    is_verified: bool


# properties returned via api
class UserPublic(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


# list of UserPublic
class UsersPublic(UserBase):
    count: int
    data: list[UserPublic]


# class to receive via API on creation
class UserCreate(UserBase):
    password: str


# class to receive via API on update
class UserUpdate(UserBase):
    password: str
