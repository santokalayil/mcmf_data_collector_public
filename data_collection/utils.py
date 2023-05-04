import json
from .paths import GCP_CREDENTIALS_JSON_PATH, CREDENTIALS_DIR

import os
from dotenv import load_dotenv


GCP_CREDENTIALS_JSON_PATH = CREDENTIALS_DIR / "google_sheet_db__datacollector.json" 

def load_cred_template() -> dict:
    TEMPLATE_JSON = CREDENTIALS_DIR / "google_sheet_db__datacollector_template.json"
    with open(TEMPLATE_JSON) as f:
        return json.load(f)

def create_gcp_credentials_json():
    load_dotenv()
    json_data = {k:os.environ[f"GCP_{k}"] for k in load_cred_template().keys()}
    with open(GCP_CREDENTIALS_JSON_PATH, 'w') as f:
        json.dump(json_data, f, sort_keys=False, indent=4)

