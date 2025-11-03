from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum as SqlEnum
import uuid
import datetime
from enum import Enum
from backend.database import Base

class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)  # уникальный
    fprint: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[RoleEnum] = mapped_column(SqlEnum(RoleEnum, name='role_enum'),nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    moments = relationship("Moment", back_populates="user", cascade="all, delete", passive_deletes=True)
    comments = relationship("Comment", back_populates="user", cascade="all, delete", passive_deletes=True)
    likes = relationship("Like", back_populates="user", cascade="all, delete", passive_deletes=True)