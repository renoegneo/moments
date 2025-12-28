from pydantic import BaseModel
import uuid


class LikeResponse(BaseModel):
    """Ответ после лайка/анлайка"""
    liked: bool
    likes_count: int