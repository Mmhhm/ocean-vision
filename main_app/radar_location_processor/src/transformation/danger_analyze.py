from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType


def calculate_hostility(speed, heat_temp, distance, size):
    # Example calculation: Higher speed and heat temperature increases hostility.
    hostility = (speed * 0.5 + heat_temp * 0.3) - (distance * 0.1) + (size * 0.05)
    return max(0, min(hostility, 100))  # Ensure the hostility is between 0 and 100

@udf(FloatType())
def calculate_danger(size, depth, speed, temp):
    # Example calculation: Larger size, slower depth, and higher speed increases danger.
    danger = (size * 0.4 + depth * 0.2 + speed * 0.3) - (temp * 0.1)
    return max(0, min(danger, 100))  # Ensure danger is between 0 and 100