from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModelBase, IdMixin, TimestampMixin


class User(IdMixin, TimestampMixin, ModelBase):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        Index=True,  # user login lookups are by email
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    portfolios: Mapped[list["Portfolio"]] = relationship(  # noqa: F821
        "Portfolio",
        back_populates="owner",
        cascade="all, delete-orphan",  # deleting a user deletes their portfolios
        lazy="selectin",  # avoids N+1 for typical user fetches
    )
