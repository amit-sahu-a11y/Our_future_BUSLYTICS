from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app import models, schemas


# =========================
# OCCUPANCY LOGIC
# =========================



def log_occupancy(db: Session, data: schemas.OccupancyUpdate):

    if data.occupancy_count < 0:
        raise HTTPException(
            status_code=400,
            detail="Occupancy count cannot be negative"
        )

    try:
        # 1️⃣ Ensure Bus exists
        bus = (
            db.query(models.Bus)
            .filter(models.Bus.bus_id == data.bus_id)
            .first()
        )

        if not bus:
            bus = models.Bus(
                bus_id=data.bus_id,
                bus_number=data.bus_id,
                route_name="UNKNOWN"
            )
            db.add(bus)

            try:
                db.commit()
                db.refresh(bus)
            except IntegrityError:
                # Another request inserted same bus simultaneously
                db.rollback()

        # 2️⃣ Insert occupancy log
        occupancy_log = models.OccupancyLog(
            bus_id=data.bus_id,
            event_type=data.event_type,
            occupancy_count=data.occupancy_count
        )
        db.add(occupancy_log)

        # 3️⃣ Update current bus state
        state = (
            db.query(models.CurrentBusState)
            .filter(models.CurrentBusState.bus_id == data.bus_id)
            .first()
        )

        if not state:
            state = models.CurrentBusState(
                bus_id=data.bus_id,
                current_occupancy=data.occupancy_count
            )
            db.add(state)
        else:
            state.current_occupancy = data.occupancy_count

        db.commit()

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Database integrity error"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# GPS LOGIC
# =========================
def log_gps(db: Session, data: schemas.GPSUpdate):

    try:
        gps_log = models.GPSLog(
            bus_id=data.bus_id,
            latitude=data.latitude,
            longitude=data.longitude
        )
        db.add(gps_log)

        state = (
            db.query(models.CurrentBusState)
            .filter(models.CurrentBusState.bus_id == data.bus_id)
            .first()
        )

        if state:
            state.last_latitude = data.latitude
            state.last_longitude = data.longitude

        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
def get_bus_state(db: Session, bus_id: str):
    return db.query(models.CurrentBusState).filter(
        models.CurrentBusState.bus_id == bus_id
    ).first()

def get_occupancy_history(db: Session, bus_id: str):
    return db.query(models.OccupancyLog).filter(
        models.OccupancyLog.bus_id == bus_id
    ).order_by(models.OccupancyLog.timestamp.desc()).all()

def get_latest_gps(db: Session, bus_id: str):
    return db.query(models.GPSLog).filter(
        models.GPSLog.bus_id == bus_id
    ).order_by(models.GPSLog.timestamp.desc()).first()


