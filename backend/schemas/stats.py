from pydantic import BaseModel


class UserStatsResponse(BaseModel):
    moments_count: int
    likes_received: int
    likes_given: int