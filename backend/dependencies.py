from sqlalchemy.orm import Session
from fastapi import Cookie, HTTPException, Depends
import uuid

from database import session_maker
from core.security import decode_token
from crud.users import get_user_by_id


def get_db():
    db = session_maker()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
        access_token: str = Cookie(None),
        db: Session = Depends(get_db)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Токен отсутствует")

    try:
        payload = decode_token(access_token)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Невалидный токен")

        user = get_user_by_id(db, uuid.UUID(user_id))

        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")

        return user

    except ValueError:
        raise HTTPException(status_code=401, detail="Невалидный токен")