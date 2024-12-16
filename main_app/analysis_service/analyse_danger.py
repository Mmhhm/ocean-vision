import math


MAX_SPEED = 30  # Max speed in knots for ships
MAX_SIZE = 1000  # Max size
MAX_DISTANCE = 10  # Maximum distance (km) for threat calculation


SPEED_THRESHOLD_GRANULARITY = 5
SIZE_THRESHOLD_GRANULARITY = 200
HEAT_SIGNATURE_GRANULARITY = 0.1
DISTANCE_GRANULARITY = 1



def calculate_hostility_score(ship):
    hostility_score = 0

    # 1. Ship Type: Military ships are more likely to be hostile
    if ship['ship_type'] in ["fighter", "military", "patrol"]:
        hostility_score += 25

    # 2. Heat Signature: High heat could indicate military technology or weaponry
    heat_score = ship['heat_signature'] * 100  # Multiply by 100 to scale to 100%
    hostility_score += heat_score

    # 3. Course Behavior: If the ship is moving towards your ship, it increases hostility
    if 170 <= ship['course'] <= 190:
        hostility_score += 20

    # 4. Weaponry: Ships with weapons are more dangerous
    if ship['weaponry']:
        hostility_score += 30

    return min(hostility_score, 100)



def calculate_danger_level_score(ship, distance_km, weather_conditions):
    danger_score = 0


    if distance_km <= 1:
        danger_score += 50  # Very close ship
    elif distance_km <= 3:
        danger_score += 40
    elif distance_km <= 5:
        danger_score += 30
    elif distance_km <= MAX_DISTANCE:
        danger_score += 20

    # 2. Speed: Faster ships are more dangerous
    speed_score = (ship['speed_knots'] / MAX_SPEED) * 40  # Normalize speed and give it a weight
    danger_score += speed_score

    # 3. Size: Larger ships are more dangerous
    size_score = (ship['size'] / MAX_SIZE) * 30  # Normalize size and apply a weight
    danger_score += size_score

    # 4. Weather Impact: Weather conditions impact the danger level
    weather_factor = 0
    if weather_conditions.get('visibility', 10000) < 5000:  # Low visibility
        weather_factor += 10  # Add danger for low visibility
    if weather_conditions.get('wind_speed', 0) > 20:  # High wind speeds
        weather_factor += 10  # Add danger for high winds
    if weather_conditions.get('humidity', 0) > 80:
        weather_factor += 5  # Add minor risk for high humidity

    danger_score += weather_factor

    return min(danger_score, 100)



def analyze_ships(ships_data, weather_conditions):
    analyzed_ships = []

    for ship in ships_data:
        # Calculate the distance to the target
        distance = math.sqrt(
            (ship['latitude'] - 34) ** 2 + (ship['longitude'] + 118) ** 2)

        # Calculate Hostility and Danger level scores
        hostility_score = calculate_hostility_score(ship)
        danger_level_score = calculate_danger_level_score(ship, distance, weather_conditions)

        # Store the results in a dictionary
        analyzed_ships.append({
            'mmsi': ship['mmsi'],
            'hostility_score': hostility_score,
            'danger_level_score': danger_level_score,
            'ship_type': ship['ship_type'],
            'distance': distance,
            'speed': ship['speed_knots'],
            'size': ship['size'],
            'heat_signature': ship['heat_signature']
        })

    return analyzed_ships


# Example ship data
ships_data = [
    {
        'mmsi': '987650001',
        'latitude': 34.0035,
        'longitude': -118.202,
        'course': 180,
        'speed_knots': 5.4,
        'size': 847,
        'heat_signature': 0.9,
        'ship_type': 'fighter',
        'weaponry': True
    },
    {
        'mmsi': '987650002',
        'latitude': 34.1465,
        'longitude': -118.1794,
        'course': 90,
        'speed_knots': 8.1,
        'size': 932,
        'heat_signature': 0.5,
        'ship_type': 'cargo',
        'weaponry': False
    }
]

# Example weather conditions
weather_conditions = {
    'visibility': 5000,  # in meters
    'wind_speed': 25,  # in knots
    'humidity': 85  # percentage
}

# Analyze ships
analyzed_ships = analyze_ships(ships_data, weather_conditions)

# Print analysis results
for ship in analyzed_ships:
    print(f"Ship {ship['mmsi']} - Hostility: {ship['hostility_score']}, Danger Level: {ship['danger_level_score']}")
