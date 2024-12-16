import json

from main_app.db_config.redis_config import redis_client
from repository.sql_repository import insert_into_ship_table, insert_into_submarine_table


def process_json_from_redis():

    for key in redis_client.scan_iter():
        # Extract the JSON data from Redis
        json_data = redis_client.get(key)
        if not json_data:
            continue

        # Parse the JSON data
        try:
            parsed_data = json.loads(json_data)
            object_type = parsed_data.get("data", {}).get("type", "unknown").lower()

            if object_type == "ship":
                insert_into_ship_table(parsed_data)
            else:
                insert_into_submarine_table(parsed_data)
        except json.JSONDecodeError:
            print(f"Failed to decode JSON for key: {key}")

