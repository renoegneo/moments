import uuid
import datetime
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base


class Comment(Base):
    __tablename__ = 'comments'

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
    text: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # связи
    user = relationship("Users", back_populates="comments")
    moment = relationship("Moment", back_populates="comments")
