from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OccupancyUpdate(BaseModel):
    bus_id: str
    event_type: str   # "IN" or "OUT"
    occupancy_count: int
    timestamp: Optional[datetime] = None


class GPSUpdate(BaseModel):
    bus_id: str
    latitude: float
    longitude: float
    timestamp: Optional[datetime] = None
