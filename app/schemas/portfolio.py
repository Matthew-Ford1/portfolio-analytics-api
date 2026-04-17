from datetime import datetime

from pydantic import BaseModel


# shared data
class PortfolioBase(BaseModel):
    name: str
    description: str | None
    currency: str
    is_default: bool


# properties returned via api
class PortfolioPublic(PortfolioBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime


# list of PortfolioPublic
class PortfoliosPublic(PortfolioBase):
    count: int
    data: list[PortfolioPublic]


# class to receive via API on creation
class PortfolioCreate(PortfolioBase):
    pass


# class to receive via API on update
class PortfolioUpdate(PortfolioBase):
    pass
