import uuid


class CallTracking():
    def __init__(self, driver):
        self.driver = driver

    def create_mother_ship(self, lat, lon):
        query = """
        CREATE (main_ship:Mother {
                id: $mother_id, lat: $lat, lon: $lon
        })
        RETURN main_ship.id as main_ship_id
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, {
                    'mother_id': 'mother_ship',
                    'lat': lat,
                    'lon': lon
                })
                return result.single()['main_ship_id']
        except Exception as e:
            print(f'Exception occurred in neo4j in creation of mother-ship: {e}')
            return None


    def add_ship(self, data):
        query = """
        CREATE (ship:Ship {
                mmsi: $mmsi, timestamp: $timestamp, lat: $lat, 
                lon: $lon, object_size: $object_size, 
                heat_temperature_celsius: $heat_temperature_celsius, 
                speed_knots: $speed_knots, bearing_degrees: $bearing_degrees,
                distance_km: $distance_km, status: $status
        })
        RETURN ship.mmsi as ship_mmsi
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, data)
                return result.single()['ship_mmsi']
        except Exception as e:
            print(f'Exception occurred while trying to add ship to neo4j: {e}')
            return None

    def add_submarine(self, data):
        query = """
        CREATE (submarine:Submarine {
                submarine_id: $submarine_id, timestamp: $timestamp, 
                lat: $lat, lon: $lon, depth_meters: $depth_meters,
                speed_knots: $speed_knots, bearing_degrees: $bearing_degrees,
                distance_km: $distance_km, status: $status, object_shape,
                 object_material: $object_material, object_size: $object_size
        })
        RETURN submarine.submarine_id as submarine_id
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, data)
                return result
        except Exception as e:
            print(f"Exception occurred while trying to add a submarine to new4j: {e}")
            return None






