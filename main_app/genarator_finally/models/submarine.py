from dataclasses import dataclass
from datetime import datetime, UTC
import random
import math


@dataclass
class Submarine:
    submarine_id: str
    latitude: float
    longitude: float
    depth: float = 0.0
    speed: float = 0.0
    heading: float = 0.0
    size: float = 0.0
    creation_time: datetime = None

    def __post_init__(self):
        if not self.depth:
            self.depth = random.uniform(100, 300)  # meters
        if not self.speed:
            self.speed = random.uniform(0, 5)  # knots
        if not self.heading:
            self.heading = random.uniform(0, 360)  # degrees
        if not self.size:
            self.size = random.uniform(400, 600)  # square meters
        if not self.creation_time:
            self.creation_time = datetime.now(UTC)

    @property
    def status(self) -> str:
        return "Moving" if self.speed > 0.5 else "Stationary"

    def move(self, time_delta_seconds: float):
        # Update depth
        self.depth += random.uniform(-10, 10)
        self.depth = max(50, min(400, self.depth))

        # Update speed
        self.speed += random.uniform(-0.5, 0.5)
        self.speed = max(0, min(5, self.speed))

        # Update heading
        self.heading += random.uniform(-5, 5)
        self.heading %= 360

        # Move if speed is sufficient
        if self.speed > 0.5:
            # Convert speed from knots to km/h and calculate distance for the time interval
            distance = (self.speed * 1.852) * (time_delta_seconds / 3600)

            # Update position
            heading_rad = math.radians(self.heading)
            self.latitude += (distance * math.cos(heading_rad)) / 111.32
            self.longitude += (distance * math.sin(heading_rad)) / (111.32 * math.cos(math.radians(self.latitude)))