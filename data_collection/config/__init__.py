import json

from ..paths import CONFIGURATION_DIR


def load_db_configuration(file:str) -> dict:
    with open(CONFIGURATION_DIR/ file) as f:
        return json.load(f)

DB_CONFIG:dict = load_db_configuration("db_sheet.json")
# DB_COLUMNS =  DB_CONFIG['columns']
DB_COLUMNS_INFO:dict = DB_CONFIG['columns']
DB_COLUMNS = list(DB_COLUMNS_INFO.keys())
