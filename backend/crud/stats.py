from sqlalchemy.orm import Session
from sqlalchemy import func
import uuid

from models.moments import Moments
from models.likes import Likes


def get_user_stats(db: Session, user_id: uuid.UUID) -> dict:
    """Статистика пользователя"""
    moments_count = db.query(func.count(Moments.id)).filter(Moments.user_id == user_id).scalar()
    
    likes_received = db.query(func.count(Likes.id)).join(
        Moments, Likes.moment_id == Moments.id
    ).filter(Moments.user_id == user_id).scalar()
    
    likes_given = db.query(func.count(Likes.id)).filter(Likes.user_id == user_id).scalar()
    
    return {
        "moments_count": moments_count or 0,
        "likes_received": likes_received or 0,
        "likes_given": likes_given or 0
    }