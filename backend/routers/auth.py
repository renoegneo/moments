from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi import Cookie, Request

from schemas.users import RegisterRequest, LoginRequest, AuthResponse, UserResponse

from crud.users import create_user, get_user_by_username, get_user_by_id
import uuid
from schemas.stats import UserStatsResponse
from crud.stats import get_user_stats

from core.security import verify_password, create_access_token, create_refresh_token, decode_token
from core.exceptions import RegistrationError
from core.rate_limit import limiter

from dependencies import get_db
from dependencies import get_current_user

from models.users import Users



router = APIRouter(prefix="/auth", tags=["Authentication"])

def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=30 * 60,
        path="/"
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=14 * 24 * 60 * 60,
        path="/"
    )
    
@router.post("/register", response_model=AuthResponse, status_code=201)
@limiter.limit("5/hour")
def register(
    request: Request,
    response: Response,
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    try:
        new_user = create_user(
            db=db,
            username=user_data.username,
            password=user_data.password,
            fprint=user_data.fprint
        )
    except RegistrationError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    
    access_token = create_access_token({"sub": str(new_user.id)})
    refresh_token = create_refresh_token({"sub": str(new_user.id)})
    
    set_auth_cookies(response, access_token, refresh_token)
    
    return AuthResponse(
        message="Регистрация успешна",
        user=UserResponse.model_validate(new_user)
    )

@router.post("/login", response_model=AuthResponse)
@limiter.limit("10/minute")
def login(
    request: Request,
    response: Response,
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    user = get_user_by_username(db, credentials.username)
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный username или пароль")
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    set_auth_cookies(response, access_token, refresh_token)
    
    return AuthResponse(
        message="Вход выполнен",
        user=UserResponse.model_validate(user)
    )


@router.post("/refresh")
def refresh_token_endpoint(
    request: Request,
    response: Response,
    refresh_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token отсутствует")
    
    try:
        payload = decode_token(refresh_token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Невалидный токен")
        
        user = get_user_by_id(db, uuid.UUID(user_id))
        
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
        
        new_access_token = create_access_token({"sub": str(user.id)})
        
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,
            samesite="none",
            max_age=30 * 60,
            path="/"
        )
        
        return {"message": "Токен обновлён"}
        
    except ValueError:
        raise HTTPException(status_code=401, detail="Невалидный токен")

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Выход выполнен"}



@router.get("/me", response_model=UserResponse)
def get_me(current_user: Users = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)

@router.get("/stats/{user_id}", response_model=UserStatsResponse)
def get_stats(
    user_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    stats = get_user_stats(db, user_id)
    return UserStatsResponse(**stats)


@router.get("/me/stats", response_model=UserStatsResponse)
def get_my_stats(
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить свою статистику"""
    stats = get_user_stats(db, current_user.id)
    return UserStatsResponse(**stats)