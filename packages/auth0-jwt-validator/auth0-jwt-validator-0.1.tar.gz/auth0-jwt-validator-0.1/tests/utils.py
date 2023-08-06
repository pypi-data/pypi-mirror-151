import json


def read_json(filepath):
    with open(filepath, encoding="utf-8") as f:
        return json.loads(f.read().encode("utf-8"))
