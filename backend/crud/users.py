from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.users import Users, RoleEnum
from core.security import hash_password
from core.exceptions import RegistrationError
import uuid


def get_user_by_username(db: Session, username: str) -> Users | None:
    return db.query(Users).filter(Users.username == username).first()


def get_user_by_id(db: Session, user_id: uuid.UUID) -> Users | None:
    return db.query(Users).filter(Users.id == user_id).first()


def get_user_by_fprint(db: Session, fprint: str) -> Users | None:
    return db.query(Users).filter(Users.fprint == fprint).first()


def get_user_by_username_or_fprint(db: Session, username: str, fprint: str) -> Users | None:
    return db.query(Users).filter(
        or_(Users.username == username, Users.fprint == fprint)
    ).first()


def create_user(
        db: Session,
        username: str,
        password: str,
        fprint: str,
        role: RoleEnum = RoleEnum.USER
) -> Users:
    existing = get_user_by_username_or_fprint(db, username, fprint)
    if existing:
        if existing.username == username:
            raise RegistrationError("Логин уже занят")
        if existing.fprint == fprint:
            raise RegistrationError("С этого устройства уже зарегистрирован аккаунт")

    hashed_password = hash_password(password)

    new_user = Users(
        username=username,
        hashed_password=hashed_password,
        fprint=fprint,
        role=role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user