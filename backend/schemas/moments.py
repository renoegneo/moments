from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from schemas.users import UserResponse


class MomentBase(BaseModel):
    text: str = Field(min_length=1, max_length=500)


class MomentCreate(MomentBase):
    image_url: str | None = Field(None, max_length=255)


class MomentResponse(MomentBase):
    id: uuid.UUID
    user_id: uuid.UUID
    image_url: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class MomentDetailResponse(MomentResponse):
    user: UserResponse
    likes_count: int = 0
    comments_count: int = 0

    class Config:
        from_attributes = True