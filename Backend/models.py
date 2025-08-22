from sqlalchemy import Column, Integer, String, Float
from .database import Base

class EnergyAsset(Base):
    __tablename__ = "energy_assets"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, unique=True)
    name = Column(String)
    price = Column(Float)
    volatility = Column(Float)
