from pydantic import BaseModel
from typing import Literal


class OccupancyUpdate(BaseModel):
    bus_id: str
    event_type: Literal["IN", "OUT"]
    occupancy_count: int


class GPSUpdate(BaseModel):
    bus_id: str
    latitude: float
    longitude: float

# class GPSUpdate(BaseModel):
#     bus_id: str

#     @validator("bus_id")
#     def normalize_bus_id(cls, v):
#         return v.upper()
#     latitude: float
#     longitude: float


