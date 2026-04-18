from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModelBase, IdMixin, TimestampMixin


class PriceHistory(IdMixin, TimestampMixin, ModelBase):
    __tablename__ = "price_history"
    _table_args__ = (
        # unique asset per date
        UniqueConstraint("asset_id", "date", name="uq_price_history_asset_date"),
        # primary access pattern: asset_id = :id AND date BETWEEN :start AND :end
        Index("ix_price_history_asset_date", "asset_id", "date"),
    )

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)

    # OHLCV — all prices in the asset's currency
    open_price: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    high_price: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    low_price: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    close_price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    adjusted_close: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    volume: Mapped[Decimal | None] = mapped_column(Numeric(20, 0), nullable=True)

    # relationship
    asset: Mapped["Asset"] = relationship(  # noqa: F821
        "Asset",
        back_populates="price_history",
        lazy="selectin",
    )
