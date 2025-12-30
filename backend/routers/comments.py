from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import uuid

from core.rate_limit import limiter
from schemas.comments import CommentCreate, CommentResponse, CommentDetailResponse
from crud.comments import create_comment, get_moment_comments, delete_comment
from crud.moments import get_moment_by_id
from models.users import Users
from dependencies import get_db, get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/{moment_id}", response_model=CommentResponse, status_code=201)
@limiter.limit("30/hour")  # 30 комментариев в час
def create_comment_endpoint(
    request: Request,
    moment_id: uuid.UUID,
    comment_data: CommentCreate,
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    moment = get_moment_by_id(db, moment_id)

    if not moment:
        raise HTTPException(status_code=404, detail="Момент не найден")

    new_comment = create_comment(
        db=db,
        moment_id=moment_id,
        user_id=current_user.id,
        text=comment_data.text
    )

    return CommentResponse.model_validate(new_comment)


@router.get("/{moment_id}", response_model=list[CommentDetailResponse])
def get_comments(
        moment_id: uuid.UUID,
        skip: int = 0,
        limit: int = 50,
        db: Session = Depends(get_db)
):
    comments = get_moment_comments(db, moment_id, skip, limit)
    return [CommentDetailResponse.model_validate(c) for c in comments]


@router.delete("/{comment_id}", status_code=204)
def delete_comment_endpoint(
        comment_id: uuid.UUID,
        current_user: Users = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    try:
        deleted = delete_comment(db, comment_id, current_user.id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Комментарий не найден")

        return None

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))