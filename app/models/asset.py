from enum import StrEnum, auto

from sqlalchemy import Enum, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModelBase, IdMixin, TimestampMixin


class AssetType(StrEnum):
    STOCK = auto()
    ETF = auto()
    CRYPTO = auto()
    FX = auto()
    OTHER = auto()


class Asset(IdMixin, TimestampMixin, ModelBase):
    __tablename__ = "assets"

    # define ticker uniquness constraint only within an exchange
    __table_args__ = {
        UniqueConstraint("ticker", "exchange", name="uq_asset_ticker_exchange"),
    }

    ticker: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    exchange: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_type: Mapped[AssetType] = mapped_column(
        Enum(AssetType, name="asset_type_enum"), nullable=False, default=AssetType.STOCK
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="AUD")

    # Relationships
    price_history: Mapped[list["PriceHistory"]] = relationship(  # noqa: F821
        "PriceHistory",
        back_populates="asset",
        cascade="all, delete-orphan",
        lazy="raise",  # always load explicitly. price history can be large
    )
    holdings: Mapped[list["Holding"]] = relationship(  # noqa: F821
        "Holding",
        back_populates="asset",
        lazy="raise",
    )
