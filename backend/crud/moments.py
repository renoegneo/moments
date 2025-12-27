from sqlalchemy.orm import Session
from sqlalchemy import desc
import uuid

from models.moments import Moments
from core.exceptions import RegistrationError


def create_moment(db: Session, user_id: uuid.UUID, text: str, image_url: str | None = None) -> Moments:
    new_moment = Moments(
        user_id=user_id,
        text=text,
        image_url=image_url
    )

    db.add(new_moment)
    db.commit()
    db.refresh(new_moment)

    return new_moment


def get_moment_by_id(db: Session, moment_id: uuid.UUID) -> Moments | None:
    return db.query(Moments).filter(Moments.id == moment_id).first()


def get_moments_feed(db: Session, skip: int = 0, limit: int = 20) -> list[Moments]:
    return db.query(Moments).order_by(desc(Moments.created_at)).offset(skip).limit(limit).all()


def get_user_moments(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 20) -> list[Moments]:
    return db.query(Moments).filter(Moments.user_id == user_id).order_by(desc(Moments.created_at)).offset(skip).limit(
        limit).all()


def delete_moment(db: Session, moment_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """Удалить момент (только владелец)"""
    moment = db.query(Moments).filter(Moments.id == moment_id).first()

    if not moment:
        return False

    if moment.user_id != user_id:
        raise PermissionError("Нельзя удалить чужой момент")

    db.delete(moment)
    db.commit()
    return True