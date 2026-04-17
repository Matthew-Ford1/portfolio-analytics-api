from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


# shared data
class HoldingBase(BaseModel):
    # high fractional quantity needed for crypto assets
    quantity: Decimal = Field(max_digits=18, decimal_places=8)
    average_cost_price: Decimal = Field(max_digits=18, decimal_places=4)
    notes: str | None


# properties returned via api
class HoldingPublic(HoldingBase):
    id: int
    portfolio_id: int
    asset_id: int
    created_at: datetime
    updated_at: datetime


# list of HoldingPublic
class HoldingsPublic(HoldingBase):
    count: int
    data: list[HoldingPublic]


# class to receive via API on creation
class HoldingCreate(HoldingBase):
    pass


# class to receive via API on update
class HoldingUpdate(HoldingBase):
    pass
