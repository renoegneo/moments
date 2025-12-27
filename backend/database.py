from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from core.config import settings

# т.к. приложение маленькое, здешний код будет синхронный
# (ну и плюс на текущий момент asyncpg не поддерживает python 3.14)
# сучка я так обломался
# по началу хотел на всех стульях усидеться
# но по итогу желание использовать последний питон меня сгубило


# асинхронный код было бы написать интереснее ес честно

DATABASE_URL = (
    f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=False, future=True)
session_maker = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
