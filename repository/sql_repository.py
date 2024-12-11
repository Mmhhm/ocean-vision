from datetime import datetime

from main_app.db_config.postgres_conn import db_session
from main_app.db_service.sql.sqlalchemy_models import ShipModel, SubmarineModel

def insert_into_ship_table(data):
    """
    Inserts data into the SHIP table.

    Args:
        data (dict): The data to insert.
    """
    ship_data = data.get("data", {})

    new_ship = ShipModel(
        type=ship_data["type"],
        mmsi=ship_data.get("submarine_id"),  # Assuming 'submarine_id' for now
        timestamp=datetime.fromisoformat(data.get("data", {}).get("timestamp")),
        lat=ship_data['detected_object']['latitude'],
        lon=ship_data['detected_object']['longitude'],
        object_size=ship_data['detected_object']["object_size"],
        heat_temperature_celsius=ship_data['detected_object']["heat_temperature_celsius"],
        hostility=ship_data['detected_object']["hostility"],
        danger=ship_data['detected_object']["danger"],
        speed_knots=ship_data['detected_object']["speed_knots"],
        bearing_degrees=ship_data['detected_object']["bearing_degrees"],
        distance_km=ship_data['detected_object']["distance_km"],
        status=ship_data['detected_object']["status"]
    )

    db_session.add(new_ship)
    db_session.commit()
    print(f"Inserted into SHIP table: {new_ship}")
    return new_ship

def insert_into_submarine_table(data):
    """
    Inserts data into the SUBMARINE table.

    Args:
        data (dict): The data to insert.
    """
    submarine_data = data.get("data", {})

    new_submarine = SubmarineModel(
        type=submarine_data["type"],
        timestamp=datetime.fromisoformat(data.get("data", {}).get("timestamp")),
        submarine_id=submarine_data['detected_object']["submarine_id"],
        object_size=submarine_data['detected_object']["object_size"],
        object_type= submarine_data['detected_object']["object_type"],
        object_shape=submarine_data['detected_object']["object_shape"],
        object_material=submarine_data['detected_object']["object_material"],
        distance_km=submarine_data['detected_object']["distance_km"],
        depth_meters=submarine_data['detected_object']["depth_meters"],
        danger=submarine_data['detected_object']["danger"],
        bearing_degrees=submarine_data['detected_object']["bearing_degrees"],
        speed_knots=submarine_data['detected_object']["speed_knots"],
        heat_temperature_celsius=submarine_data['detected_object']["heat_temperature_celsius"],
        hostility=submarine_data['detected_object']["hostility"],
        status=submarine_data['detected_object']["status"],
        lat=submarine_data['detected_object']["lat"],
        lon=submarine_data['detected_object']["lon"],
    )
    db_session.add(new_submarine)
    db_session.commit()
    print(f"Inserting into SUBMARINE table: {data}")
    return new_submarine