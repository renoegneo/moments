from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from schemas.likes import LikeResponse
from crud.likes import add_like, remove_like, get_moment_likes_count, check_user_liked
from crud.moments import get_moment_by_id
from models.users import Users
from dependencies import get_db, get_current_user

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/{moment_id}", response_model=LikeResponse)
def toggle_like(
        moment_id: uuid.UUID,
        current_user: Users = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    moment = get_moment_by_id(db, moment_id)

    if not moment:
        raise HTTPException(status_code=404, detail="Момент не найден")

    is_liked = check_user_liked(db, moment_id, current_user.id)

    if is_liked:
        remove_like(db, moment_id, current_user.id)
        liked = False
    else:
        add_like(db, moment_id, current_user.id)
        liked = True

    likes_count = get_moment_likes_count(db, moment_id)

    return LikeResponse(liked=liked, likes_count=likes_count)


@router.get("/{moment_id}/count")
def get_likes_count(
        moment_id: uuid.UUID,
        db: Session = Depends(get_db)
):
    count = get_moment_likes_count(db, moment_id)
    return {"likes_count": count}


@router.get("/{moment_id}/check")
def check_like_status(
        moment_id: uuid.UUID,
        current_user: Users = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    liked = check_user_liked(db, moment_id, current_user.id)
    return {"liked": liked}