from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from schemas.users import UserResponse


class CommentCreate(BaseModel):
    text: str = Field(min_length=1, max_length=300)


class CommentResponse(BaseModel):
    id: uuid.UUID
    moment_id: uuid.UUID
    user_id: uuid.UUID
    text: str
    created_at: datetime

    class Config:
        from_attributes = True


class CommentDetailResponse(CommentResponse):
    user: UserResponse

    class Config:
        from_attributes = True