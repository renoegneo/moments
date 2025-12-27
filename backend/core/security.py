import bcrypt
from datetime import timedelta, datetime, timezone
from jose import JWTError, jwt
from core.config import settings


def hash_password(pswd: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pswd.encode('utf-8'), salt)
    # тупые пиндосы сделали бкрипт битовым, надо кодировку указывать
    return hashed.decode('utf-8')

def verify_password(plain_pswd: str, hashed_pswd: str) -> bool:
    return bcrypt.checkpw(plain_pswd.encode('utf-8'), hashed_pswd.encode('utf-8'))

def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# подфункции аля дочки
def create_access_token(data: dict) -> str:
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_token(data, expires_delta)


def create_refresh_token(data: dict) -> str:
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return create_token(data, expires_delta)





def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise ValueError("Невалидный токен")


