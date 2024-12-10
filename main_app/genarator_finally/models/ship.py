from dataclasses import dataclass
import random
import math
from datetime import datetime, UTC

@dataclass
class Ship:
    mmsi: str
    latitude: float
    longitude: float
    speed: float = 0.0
    heading: float = 0.0
    size: float = 0.0
    heat_signature: float = 0.0
    creation_time: datetime = None

    def __post_init__(self):
        if not self.speed:
            self.speed = random.uniform(5, 15)  # knots
        if not self.heading:
            self.heading = random.uniform(0, 360)  # degrees
        if not self.size:
            self.size = random.uniform(300, 1000)  # square meters
        if not self.heat_signature:
            self.heat_signature = random.uniform(35, 45)  # celsius
        if not self.creation_time:
            self.creation_time = datetime.now(UTC)

    def move(self, time_delta_seconds: float):
        # Calculate distance in km based on speed and time
        distance = (self.speed * 1.852) * (time_delta_seconds / 3600)

        # Update position
        heading_rad = math.radians(self.heading)
        self.latitude += (distance * math.cos(heading_rad)) / 111.32
        self.longitude += (distance * math.sin(heading_rad)) / (111.32 * math.cos(math.radians(self.latitude)))

        # Random small changes in speed and direction
        self.speed += random.uniform(-0.5, 0.5)
        self.speed = max(1, min(20, self.speed))
        self.heading += random.uniform(-5, 5)
        self.heading %= 360

        # Random changes in heat signature
        self.heat_signature += random.uniform(-0.2, 0.2)
        self.heat_signature = max(30, min(50, self.heat_signature))