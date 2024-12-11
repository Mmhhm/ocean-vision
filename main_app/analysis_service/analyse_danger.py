import math

# Define constants for threat evaluation with finer granularity
MAX_SPEED = 30  # Max speed in knots for ships
MAX_SIZE = 1000  # Max size (in terms of tonnage or volume)
MAX_DISTANCE = 10  # Maximum distance (km) for threat calculation

# Thresholds and weightings for finer resolution
SPEED_THRESHOLD_GRANULARITY = 5  # 5 knot intervals for speed impact
SIZE_THRESHOLD_GRANULARITY = 200  # 200-ton intervals for size impact
HEAT_SIGNATURE_GRANULARITY = 0.1  # 0.1 resolution for heat signature
DISTANCE_GRANULARITY = 1  # 1 km intervals for distance impact


# Function to calculate the hostility score with finer granularity
def calculate_hostility_score(ship):
    hostility_score = 0

    # 1. Ship Type: Military ships are more likely hostile
    if ship['ship_type'] in ["fighter", "military", "patrol"]:
        hostility_score += 25  # Significant hostility score for military ship types

    # 2. Heat Signature: High heat could indicate military-grade technology or weaponry
    heat_score = ship['heat_signature'] * 100  # Multiply by 100 to scale to 100%
    hostility_score += heat_score

    # 3. Course Behavior: If the ship is moving towards your ship, it increases hostility
    if 170 <= ship['course'] <= 190:  # Assume course between 170° and 190° indicates movement towards
        hostility_score += 20  # Aggressive behavior heading towards the ship

    # 4. Weaponry: Ships with weapons are more dangerous
    if ship['weaponry']:
        hostility_score += 30  # Add 30 points for weaponized ships

    return min(hostility_score, 100)  # Cap the hostility score at 100


# Function to calculate the danger level score with higher granularity
def calculate_danger_level_score(ship, distance_km, weather_conditions):
    danger_score = 0

    # 1. Proximity: Ships closer to your ship are more dangerous (more granular)
    if distance_km <= 1:
        danger_score += 50  # Very close ship (imminent threat)
    elif distance_km <= 3:
        danger_score += 40  # Close proximity ship
    elif distance_km <= 5:
        danger_score += 30  # Moderate proximity ship
    elif distance_km <= MAX_DISTANCE:
        danger_score += 20  # Ship further out, but still a danger

    # 2. Speed: Faster ships are more dangerous (granular speed impact)
    speed_score = (ship['speed_knots'] / MAX_SPEED) * 40  # Normalize speed and give it a weight
    danger_score += speed_score

    # 3. Size: Larger ships are more dangerous (continuous scale for size)
    size_score = (ship['size'] / MAX_SIZE) * 30  # Normalize size and apply a weight
    danger_score += size_score

    # 4. Weather Impact: Weather conditions impact the danger level (fine-grained weather factors)
    weather_factor = 0
    if weather_conditions.get('visibility', 10000) < 5000:  # Low visibility (below 5km)
        weather_factor += 10  # Add danger for low visibility
    if weather_conditions.get('wind_speed', 0) > 20:  # High wind speeds (over 20 knots)
        weather_factor += 10  # Add danger for high winds
    if weather_conditions.get('humidity', 0) > 80:  # High humidity could cause radar malfunction
        weather_factor += 5  # Add minor risk for high humidity

    danger_score += weather_factor

    return min(danger_score, 100)  # Cap the danger score at 100


# Example of how to use the functions:
def analyze_ships(ships_data, weather_conditions):
    analyzed_ships = []

    for ship in ships_data:
        # Calculate the distance to the target (simplified, using coordinates)
        distance = math.sqrt(
            (ship['latitude'] - 34) ** 2 + (ship['longitude'] + 118) ** 2)  # Simplified distance formula

        # Calculate Hostility and Danger level scores with higher resolution
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


# Example ship data (simplified)
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

# Example weather conditions (simplified)
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
