from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base


class Bus(Base):
    __tablename__ = "buses"

    bus_id = Column(String, primary_key=True, index=True)
    bus_number = Column(String)
    route_name = Column(String)


class OccupancyLog(Base):
    __tablename__ = "occupancy_logs"

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(String, ForeignKey("buses.bus_id"))
    event_type = Column(String)
    occupancy_count = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class GPSLog(Base):
    __tablename__ = "gps_logs"

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(String, ForeignKey("buses.bus_id"))
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class CurrentBusState(Base):
    __tablename__ = "current_bus_state"

    bus_id = Column(String, ForeignKey("buses.bus_id"), primary_key=True)
    current_occupancy = Column(Integer, default=0)
    last_latitude = Column(Float, nullable=True)
    last_longitude = Column(Float, nullable=True)
