from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import uuid

from schemas.users import UserResponse


class MomentBase(BaseModel):
    text: str = Field(min_length=1, max_length=500, description="Текст момента")


class MomentCreate(MomentBase):
    image_url: str | None = Field(None, max_length=255, description="URL изображения (опционально)")


class MomentResponse(MomentBase):
    id: uuid.UUID
    user_id: uuid.UUID
    image_url: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MomentDetailResponse(MomentResponse):
    user: UserResponse

    model_config = ConfigDict(from_attributes=True)