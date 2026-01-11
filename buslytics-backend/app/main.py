print("MAIN FILE LOADED FROM:", __file__)

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from . import schemas, crud  # ✅ schemas imported correctly

# ✅ THIS IS THE ONLY CORRECT TABLE CREATION
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BUSLYTICS Backend")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/occupancy/update")
def update_occupancy(
    data: schemas.OccupancyUpdate,
    db: Session = Depends(get_db)
):
    crud.log_occupancy(db, data)
    return {"status": "occupancy updated"}

@app.post("/api/gps/update")
def update_gps(
    data: schemas.GPSUpdate,
    db: Session = Depends(get_db)
):
    crud.log_gps(db, data)
    return {"status": "gps updated"}
