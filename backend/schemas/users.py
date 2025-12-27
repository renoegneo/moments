from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import uuid


class UserBase(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=30
    )


class RegisterRequest(UserBase):
    password: str = Field(
        min_length=6,
        max_length=100
    )
    fprint: str = Field(
        min_length=1
    )


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=6, max_length=100)


class UserResponse(UserBase):
    id: uuid.UUID
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuthResponse(BaseModel):
    message: str
    user: UserResponse