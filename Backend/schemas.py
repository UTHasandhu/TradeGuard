from pydantic import BaseModel

class AssetBase(BaseModel):
    symbol: str
    name: str

class AssetCreate(AssetBase):
    pass

class Asset(AssetBase):
    id: int
    price: float | None = None
    volatility: float | None = None

    class Config:
        orm_mode = True
