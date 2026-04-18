from sqlalchemy import Boolean, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import IdMixin, ModelBase, TimestampMixin


class Portfolio(IdMixin, TimestampMixin, ModelBase):
    __tablename__ = "portfolios"

    __table_args__ = (UniqueConstraint("owner_id", "name", name="uq_user_portfolio_name"),)

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="AUD")
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # relationships
    owner: Mapped["User"] = relationship(  # noqa: F821
        "User",
        back_populates="portfolios",
        lazy="selectin",
    )
    holdings: Mapped[list["Holding"]] = relationship(  # noqa: F821
        "Holding",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
