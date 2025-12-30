from sqlalchemy.orm import Session
from sqlalchemy import desc
import uuid

from models.comments import Comments


def create_comment(db: Session, moment_id: uuid.UUID, user_id: uuid.UUID, text: str) -> Comments:
    new_comment = Comments(
        moment_id=moment_id,
        user_id=user_id,
        text=text
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


def get_moment_comments(db: Session, moment_id: uuid.UUID, skip: int = 0, limit: int = 50):
    return db.query(Comments).filter(
        Comments.moment_id == moment_id
    ).order_by(Comments.created_at).offset(skip).limit(limit).all()


def delete_comment(db: Session, comment_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    comment = db.query(Comments).filter(Comments.id == comment_id).first()

    if not comment:
        return False

    if comment.user_id != user_id:
        raise PermissionError("Нельзя удалить чужой комментарий")

    db.delete(comment)
    db.commit()
    return True