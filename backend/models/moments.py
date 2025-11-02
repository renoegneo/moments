import uuid
import datetime
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base


class Moment(Base):
    __tablename__ = 'moments'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # связи
    user = relationship("Users", back_populates="moments", passive_deletes=True)
    comments = relationship("Comment", back_populates="moment", cascade="all, delete", passive_deletes=True)
    likes = relationship("Like", back_populates="moment", cascade="all, delete", passive_deletes=True)
