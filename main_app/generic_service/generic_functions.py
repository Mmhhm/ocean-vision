import json


def save_dict_to_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)
    print(f"Saved data to {path}")

