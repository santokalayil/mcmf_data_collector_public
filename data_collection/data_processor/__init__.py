import json
from ..paths import DATA_DIR
from ..config import DB_COLUMNS_INFO

def load_regionwise_parishes_data() -> dict:
    REGIONWISE_PARISHES_JSON = DATA_DIR / "parishes.json"
    with open(REGIONWISE_PARISHES_JSON, "r") as f:
        return json.load(f)
    

PARISHES = load_regionwise_parishes_data()


def find_region(parish) -> str:
    global PARISHES
    for region, parishes in PARISHES.items():
        if parish in parishes:
            return region
    else:
        raise Exception(f"The parish '{parish}' is not found in any regions available")


def get_parishes_in_the_region(region) -> list:
    if region in PARISHES.keys():
        return PARISHES[region]
    else:
        raise Exception(f"The region '{region}' is not found")


def serialize_data(data):
    for col, params in DB_COLUMNS_INFO.items():
        if col in data:
            if params['type'] == 'date':
                data[col] = data[col].strftime("%b %d %Y")
    return data

