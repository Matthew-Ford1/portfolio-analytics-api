from datetime import datetime

from pydantic import BaseModel, Field

from app.models.asset import AssetType


# shared data
class AssetBase(BaseModel):
    ticker: str = Field(max_length=20)
    exchange: str = Field(max_length=20)
    name: str
    asset_type: AssetType
    currency: str = Field(max_length=3, min_length=3)


# properties returned via api
class AssetPublic(AssetBase):
    id: int
    created_at: datetime
    updated_at: datetime


# list of AssetPublic
class AssetsPublic(AssetBase):
    count: int
    data: list[AssetPublic]


# class to receive via API on creation
class AssetCreate(AssetBase):
    pass


# class to receive via API on update
class AssetUpdate(AssetBase):
    pass
