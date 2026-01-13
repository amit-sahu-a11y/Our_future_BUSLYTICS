print("MAIN FILE LOADED FROM:", __file__)

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from . import schemas, crud  # ✅ schemas imported correctly
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
@app.get("/api/bus/state/{bus_id}")
def get_bus_state(bus_id: str, db: Session = Depends(get_db)):
    state = crud.get_bus_state(db, bus_id)

    if not state:
        raise HTTPException(status_code=404, detail="Bus not found")

    return {
        "bus_id": bus_id,
        "current_occupancy": state.current_occupancy,
        "latitude": state.last_latitude,
        "longitude": state.last_longitude
    }

@app.get("/api/occupancy/history/{bus_id}")
def occupancy_history(bus_id: str, db: Session = Depends(get_db)):
    logs = crud.get_occupancy_history(db, bus_id)

    return [
        {
            "event_type": log.event_type,
            "occupancy_count": log.occupancy_count,
            "timestamp": log.timestamp
        }
        for log in logs
    ]

@app.get("/api/gps/latest/{bus_id}")
def latest_gps(bus_id: str, db: Session = Depends(get_db)):
    gps = crud.get_latest_gps(db, bus_id)

    if not gps:
        raise HTTPException(status_code=404, detail="No GPS data found")

    return {
        "bus_id": bus_id,
        "latitude": gps.latitude,
        "longitude": gps.longitude,
        "timestamp": gps.timestamp
    }


