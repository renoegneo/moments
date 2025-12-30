from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from schemas.moments import MomentCreate, MomentResponse, MomentDetailResponse
from schemas.users import UserResponse
from crud.moments import (
    create_moment,
    get_moment_by_id,
    get_moments_feed,
    get_user_moments,
    delete_moment,
    search_moments  # добавь
)

from models.users import Users
from dependencies import get_db, get_current_user

router = APIRouter(prefix="/moments", tags=["Moments"])


@router.post("", response_model=MomentResponse, status_code=201)
def create_moment_endpoint(
        moment_data: MomentCreate,
        current_user: Users = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    new_moment = create_moment(
        db=db,
        user_id=current_user.id,
        text=moment_data.text,
        image_url=moment_data.image_url
    )
    return MomentResponse.model_validate(new_moment)


@router.get("/feed", response_model=list[MomentDetailResponse])
def get_feed(
        skip: int = 0,
        limit: int = 20,
        db: Session = Depends(get_db)
):
    moments = get_moments_feed(db, skip, limit)
    return [MomentDetailResponse.model_validate(m) for m in moments]


@router.get("/{moment_id}", response_model=MomentDetailResponse)
def get_moment(
        moment_id: uuid.UUID,
        db: Session = Depends(get_db)
):
    moment = get_moment_by_id(db, moment_id)

    if not moment:
        raise HTTPException(status_code=404, detail="Момент не найден")

    return MomentDetailResponse.model_validate(moment)


@router.get("/user/{user_id}", response_model=list[MomentDetailResponse])
def get_user_moments_endpoint(
        user_id: uuid.UUID,
        skip: int = 0,
        limit: int = 20,
        db: Session = Depends(get_db)
):
    moments = get_user_moments(db, user_id, skip, limit)
    return [MomentDetailResponse.model_validate(m) for m in moments]


@router.delete("/{moment_id}", status_code=204)
def delete_moment_endpoint(
        moment_id: uuid.UUID,
        current_user: Users = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    try:
        deleted = delete_moment(db, moment_id, current_user.id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Момент не найден")

        return None

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/search", response_model=list[MomentDetailResponse])
def search_moments_endpoint(
        q: str,
        skip: int = 0,
        limit: int = 20,
        db: Session = Depends(get_db)
):
    if len(q) < 2:
        raise HTTPException(status_code=400, detail="Запрос должен быть минимум 2 символа")

    moments = search_moments(db, q, skip, limit)
    return [MomentDetailResponse.model_validate(m) for m in moments]