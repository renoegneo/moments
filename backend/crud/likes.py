from sqlalchemy.orm import Session
from sqlalchemy import and_
import uuid

from models.likes import Likes


def add_like(db: Session, moment_id: uuid.UUID, user_id: uuid.UUID) -> Likes | None:
    existing = db.query(Likes).filter(
        and_(Likes.moment_id == moment_id, Likes.user_id == user_id)
    ).first()

    if existing:
        return None

    new_like = Likes(moment_id=moment_id, user_id=user_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    return new_like


def remove_like(db: Session, moment_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    like = db.query(Likes).filter(
        and_(Likes.moment_id == moment_id, Likes.user_id == user_id)
    ).first()

    if not like:
        return False

    db.delete(like)
    db.commit()
    return True


def get_moment_likes_count(db: Session, moment_id: uuid.UUID) -> int:
    return db.query(Likes).filter(Likes.moment_id == moment_id).count()


def check_user_liked(db: Session, moment_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    like = db.query(Likes).filter(
        and_(Likes.moment_id == moment_id, Likes.user_id == user_id)
    ).first()
    return like is not None