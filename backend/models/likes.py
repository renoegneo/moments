import uuid
import datetime
from sqlalchemy import DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base


class Likes(Base):
    __tablename__ = 'likes'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    moment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('moments.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # связи
    user = relationship("Users", back_populates="likes")
    moment = relationship("Moments", back_populates="likes")

    # один пользователь может лайкнуть один момент только один раз
    __table_args__ = (
        UniqueConstraint('moment_id', 'user_id', name='unique_moment_user_like'),
    )