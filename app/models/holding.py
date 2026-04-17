from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModelBase, IdMixin, TimestampMixin


class Holding(IdMixin, TimestampMixin, ModelBase):
    __tablename__ = "holdings"

    # A portfolio can only hold one position per asset.
    __table_args__ = (UniqueConstraint("portfolio_id", "asset_id", name="uq_holding_portfolio_asset"),)

    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False, index=True
    )
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    # high fractional quantity needed for crypto assets
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)

    # weighted average purchase price
    average_cost_price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # relationships
    portfolio: Mapped["Portfolio"] = relationship(  # noqa: F821
        "Portfolio",
        back_populates="holdings",
        lazy="selectin",
    )
    asset: Mapped["Asset"] = relationship(  # noqa: F821
        "Asset",
        back_populates="holdings",
        lazy="selectin",  # almost always needed alongside the holding
    )
