from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, services
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Energy Risk Dashboard")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/assets/", response_model=schemas.Asset)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    db_asset = db.query(models.EnergyAsset).filter(models.EnergyAsset.symbol == asset.symbol).first()
    if db_asset:
        raise HTTPException(status_code=400, detail="Asset already exists")

    data = services.fetch_asset_data(asset.symbol)
    new_asset = models.EnergyAsset(
        symbol=asset.symbol,
        name=asset.name,
        price=data["price"],
        volatility=data["volatility"]
    )
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset

@app.get("/assets/{symbol}", response_model=schemas.Asset)
def get_asset(symbol: str, db: Session = Depends(get_db)):
    db_asset = db.query(models.EnergyAsset).filter(models.EnergyAsset.symbol == symbol).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset
