from sqlalchemy.orm import Session
from sqlalchemy import desc, func
import uuid

from models.moments import Moments
from models.comments import Comments
from models.likes import Likes


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


def get_user_moments(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 20):
    results = db.query(
        Moments,
        func.count(Likes.id.distinct()).label('likes_count'),
        func.count(Comments.id.distinct()).label('comments_count')
    ).outerjoin(Likes, Likes.moment_id == Moments.id
                ).outerjoin(Comments, Comments.moment_id == Moments.id
                            ).filter(Moments.user_id == user_id
                                     ).group_by(Moments.id
                                                ).order_by(desc(Moments.created_at)
                                                           ).offset(skip).limit(limit).all()

    moments = []
    for moment, likes_count, comments_count in results:
        moment.likes_count = likes_count
        moment.comments_count = comments_count
        moments.append(moment)

    return moments


def get_moment_by_id(db: Session, moment_id: uuid.UUID) -> Moments | None:
    result = db.query(
        Moments,
        func.count(Likes.id.distinct()).label('likes_count'),
        func.count(Comments.id.distinct()).label('comments_count')
    ).outerjoin(Likes, Likes.moment_id == Moments.id
                ).outerjoin(Comments, Comments.moment_id == Moments.id
                            ).filter(Moments.id == moment_id
                                     ).group_by(Moments.id
                                                ).first()

    if not result:
        return None

    moment, likes_count, comments_count = result
    moment.likes_count = likes_count
    moment.comments_count = comments_count

    return moment


def get_moments_feed(db: Session, skip: int = 0, limit: int = 20):
    results = db.query(
        Moments,
        func.count(Likes.id.distinct()).label('likes_count'),
        func.count(Comments.id.distinct()).label('comments_count')
    ).outerjoin(Likes, Likes.moment_id == Moments.id
                ).outerjoin(Comments, Comments.moment_id == Moments.id
                            ).group_by(Moments.id
                                       ).order_by(desc(Moments.created_at)
                                                  ).offset(skip).limit(limit).all()

    moments = []
    for moment, likes_count, comments_count in results:
        moment.likes_count = likes_count
        moment.comments_count = comments_count
        moments.append(moment)

    return moments



def delete_moment(db: Session, moment_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    moment = db.query(Moments).filter(Moments.id == moment_id).first()

    if not moment:
        return False

    if moment.user_id != user_id:
        raise PermissionError("Ты как бля это сделать умудрился")

    db.delete(moment)
    db.commit()
    return True


def search_moments(db: Session, query: str, skip: int = 0, limit: int = 20):
    search_pattern = f"%{query}%"

    results = db.query(
        Moments,
        func.count(Likes.id.distinct()).label('likes_count'),
        func.count(Comments.id.distinct()).label('comments_count')
    ).outerjoin(Likes, Likes.moment_id == Moments.id
                ).outerjoin(Comments, Comments.moment_id == Moments.id
                            ).filter(Moments.text.ilike(search_pattern)
                                     ).group_by(Moments.id
                                                ).order_by(desc(Moments.created_at)
                                                           ).offset(skip).limit(limit).all()

    moments = []
    for moment, likes_count, comments_count in results:
        moment.likes_count = likes_count
        moment.comments_count = comments_count
        moments.append(moment)

    return moments

def get_moments_total(db: Session) -> int:
    return db.query(func.count(Moments.id)).scalar()


def get_user_moments_total(db: Session, user_id: uuid.UUID) -> int:
    return db.query(func.count(Moments.id)).filter(Moments.user_id == user_id).scalar()


def search_moments_total(db: Session, query: str) -> int:
    search_pattern = f"%{query}%"
    return db.query(func.count(Moments.id)).filter(Moments.text.ilike(search_pattern)).scalar()
