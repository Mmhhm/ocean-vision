from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from base_model import Base


# Todo make sure the analyzed data is inserted into the tables
# Thermal Sensor Data Model
class ShipData(Base):
    __tablename__ = 'thermal_sensor_data'

    id = Column(Integer, primary_key=True)
    mmsi = Column(String)  # MMSI of the detected ship
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    lat = Column(Float, nullable=False)  # Latitude of the detected object
    lon = Column(Float, nullable=False)  # Longitude of the detected object
    object_size = Column(Integer)  # Size of the detected object (e.g., m^2 or numeric)
    heat_temperature_celsius = Column(Float)  # Temperature of the detected object (in Celsius)
    speed_knots = Column(Float)  # Speed of the object (in knots)
    bearing_degrees = Column(Float)  # Bearing in degrees
    distance_km = Column(Float)  # Distance from the thermal sensor (in km)
    status = Column(String)  # e.g., "Moving", "Stationary"


# Sonar Sensor Data Model (Updated with object_shape and object_material)
class SubmarineData(Base):
    __tablename__ = 'sonar_sensor_data'

    id = Column(Integer, primary_key=True)
    submarine_id = Column(String)  # Submarine ID if applicable (e.g., "SUB0001")
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    lat = Column(Float, nullable=False)  # Latitude of the detected object
    lon = Column(Float, nullable=False)  # Longitude of the detected object
    depth_meters = Column(Float)  # Depth of the detected object (in meters)
    speed_knots = Column(Float)  # Speed of the object (in knots)
    bearing_degrees = Column(Float)  # Bearing in degrees
    distance_km = Column(Float)  # Distance from the sonar (in km)
    status = Column(String)  # e.g., "Moving", "Stationary"
    object_shape = Column(String)  # Shape of the detected object (e.g., "Cylindrical")
    object_material = Column(String)  # Material of the detected object (e.g., "Metal")
    object_size = Column(Integer)  # Size of the detected object (e.g., m^2 or numeric)

# WeatherData Model (based on the weather data in the JSON)
class WeatherData(Base):
    __tablename__ = 'weather_data'

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

