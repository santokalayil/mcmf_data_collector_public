import json
from ..paths import DATA_DIR

def load_regionwise_parishes_data():
    REGIONWISE_PARISHES_JSON = DATA_DIR / "parishes.json"
    with open(REGIONWISE_PARISHES_JSON, "r") as f:
        return json.load(f)