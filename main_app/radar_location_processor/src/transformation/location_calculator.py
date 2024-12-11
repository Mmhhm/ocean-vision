import math

def calculate_location(lat1, lon1, distance_km, bearing_degrees):
    R = 6371  
    bearing = math.radians(bearing_degrees)
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.asin(
        math.sin(lat1) * math.cos(distance_km / R) +
        math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing)
    )

    lon2 = lon1 + math.atan2(
        math.sin(bearing) * math.sin(distance_km / R) * math.cos(lat1),
        math.cos(distance_km / R) - math.sin(lat1) * math.sin(lat2)
    )

    return math.degrees(lat2), math.degrees(lon2)
