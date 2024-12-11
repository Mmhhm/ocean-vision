from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from base_model import Base


# Todo make sure the analyzed data is inserted into the tables
# Thermal Sensor Data Model
class ShipModel(Base):
    __tablename__ = 'ships'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    mmsi = Column(String)  # MMSI of the detected ship
    timestamp = Column(DateTime, default=datetime.now(), nullable=False)
    lat = Column(Float, nullable=False)  # Latitude of the detected object
    lon = Column(Float, nullable=False)  # Longitude of the detected object
    object_size = Column(Integer)  # Size of the detected object (e.g., m^2 or numeric)
    heat_temperature_celsius = Column(Float)  # Temperature of the detected object (in Celsius)
    hostility = Column(Float)
    danger = Column(Float)
    speed_knots = Column(Float)  # Speed of the object (in knots)
    bearing_degrees = Column(Float)  # Bearing in degrees
    distance_km = Column(Float)  # Distance from the thermal sensor (in km)
    status = Column(String)  # e.g., "Moving", "Stationary"

# Sonar Sensor Data Model (Updated with object_shape and object_material)
class SubmarineModel(Base):
    __tablename__ = 'Submarines'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    submarine_id = Column(String)  # Submarine ID if applicable (e.g., "SUB0001")
    timestamp = Column(DateTime, default=datetime.now(), nullable=False)
    lat = Column(Float, nullable=False)  # Latitude of the detected object
    lon = Column(Float, nullable=False)  # Longitude of the detected object
    depth_meters = Column(Float)  # Depth of the detected object (in meters)
    danger = Column(Float)
    distance_km = Column(Float)  # Distance from the sonar (in km)
    bearing_degrees = Column(Float)  # Bearing in degrees
    heat_temperature_celsius = Column(Float)
    hostility = Column(Integer)
    status = Column(String)  # e.g., "Moving", "Stationary"
    object_type = Column(String)
    object_shape = Column(String)  # Shape of the detected object (e.g., "Cylindrical")
    object_material = Column(String)  # Material of the detected object (e.g., "Metal")
    object_size = Column(Integer)  # Size of the detected object (e.g., m^2 or numeric)
    speed_knots = Column(Float)  # Speed of the object (in knots)

# WeatherData Model (based on the weather data in the JSON)
class WeatherModel(Base):
    __tablename__ = 'the_weather'

    id = Column(Integer, primary_key=True)
    sensor_id = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)

    temp = Column(Float, nullable=True)  # Fahrenheit

    weather_main = Column(String, nullable=True)  # e.g., "Clouds"
    weather_description = Column(String, nullable=True)  # e.g., "overcast clouds"
    weather_icon = Column(String, nullable=True)  # e.g., "04d"

    wind_speed = Column(Float, nullable=True)
    wind_deg = Column(Float, nullable=True)
    wind_gust = Column(Float, nullable=True)
    visibility = Column(Integer, nullable=True)
    pressure = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)