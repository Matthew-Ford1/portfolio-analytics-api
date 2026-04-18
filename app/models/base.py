from datetime import datetime

from sqlalchemy import DateTime, Identity, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class ModelBase(DeclarativeBase):
    """
    Single declarative base for entire app db.
    """

    pass


class IdMixin:
    """
    Server-side generated identity as primary key.
    """

    id: Mapped[int] = mapped_column(Identity(start=100), primary_key=True, sort_order=-10)


class TimestampMixin:
    """
    Audit timestamps maintained by the database, not application code.
    - created_at: set once on INSERT via server default
    - updated_at: updated automatically on every UPDATE via onupdate
    Using server-side defaults means the columns are correct even for
    bulk inserts that bypass the ORM layer.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
