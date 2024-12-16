import redis
import json
from main_app.db_config.redis_config import redis_client

def save_full_json_to_redis(json_data):

    data = json_data.get("data", {})
    object_type = data.get("type", "unknown").lower()
    timestamp = data.get("timestamp", "unknown")
    detected_object = data.get("detected_object", {})

    # Create a unique key for the object
    object_id = detected_object.get(f"{object_type}_id", "unknown")
    redis_key = f"{object_type}:{object_id}:{timestamp}"

    # Save the JSON to Redis
    redis_client.set(redis_key, json.dumps(json_data))
    print(f"Full JSON data saved to Redis with key: {redis_key}")