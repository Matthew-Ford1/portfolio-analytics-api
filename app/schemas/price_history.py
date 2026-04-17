from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


# shared data
class PriceHistoryBase(BaseModel):
    date: datetime

    open_price: Decimal
    high_price: Decimal
    low_price: Decimal
    close_price: Decimal
    adjusted_close: Decimal
    volume: int


# properties returned via api
class PriceHistoryPublic(PriceHistoryBase):
    id: int
    asset_id: int
    created_at: datetime
    updated_at: datetime


# list of PriceHistoryPublic
class PriceHistorysPublic(PriceHistoryBase):
    count: int
    data: list[PriceHistoryPublic]


# class to receive via API on creation
class PriceHistoryCreate(PriceHistoryBase):
    pass


# class to receive via API on update
class PriceHistoryUpdate(PriceHistoryBase):
    pass
