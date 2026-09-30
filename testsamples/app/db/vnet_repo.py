import json
import os

DB_FILE = "resource_store.json"

def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)

def save_resource(resource_id: str, data: dict):
    init_db()
    with open(DB_FILE, "r+") as f:
        db = json.load(f)
        db[resource_id] = data
        f.seek(0)
        json.dump(db, f, indent=4)
        f.truncate()

def get_resource(resource_id: str) -> dict:
    init_db()
    with open(DB_FILE, "r") as f:
        return json.load(f).get(resource_id)

def get_all_resources() -> dict:
    init_db()
    with open(DB_FILE, "r") as f:
        return json.load(f)
