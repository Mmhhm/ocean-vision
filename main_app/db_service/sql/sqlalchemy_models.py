from ctypes.wintypes import BOOLEAN

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from base_model import Base



class ShipModel(Base):
    __tablename__ = 'ships'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    mmsi = Column(String)
    timestamp = Column(DateTime, default=datetime.now(), nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    object_size = Column(Integer)
    heat_temperature_celsius = Column(Float)
    hostility = Column(Boolean)
    danger = Column(Float)
    speed_knots = Column(Float)
    bearing_degrees = Column(Float)
    distance_km = Column(Float)
    status = Column(String)


class SubmarineModel(Base):
    __tablename__ = 'Submarines'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    submarine_id = Column(String)
    timestamp = Column(DateTime, default=datetime.now(), nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    depth_meters = Column(Float)
    danger = Column(Float)
    distance_km = Column(Float)
    bearing_degrees = Column(Float)
    heat_temperature_celsius = Column(Float)
    hostility = Column(Boolean)
    status = Column(String)
    object_type = Column(String)
    object_shape = Column(String)
    object_material = Column(String)
    object_size = Column(Integer)
    speed_knots = Column(Float)


class WeatherModel(Base):
    __tablename__ = 'the_weather'

    id = Column(Integer, primary_key=True)
    sensor_id = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)

    temp = Column(Float, nullable=True)

    weather_main = Column(String, nullable=True)
    weather_description = Column(String, nullable=True)
    weather_icon = Column(String, nullable=True)

    wind_speed = Column(Float, nullable=True)
    wind_deg = Column(Float, nullable=True)
    wind_gust = Column(Float, nullable=True)
    visibility = Column(Integer, nullable=True)
    pressure = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)