from pathlib import Path
from dotenv import load_dotenv
import os

from ..paths import CREDENTIALS_DIR


load_dotenv()

# to configuration file
GOOGLE_CREDS_FILE = "google_sheet_db__datacollector.json"

SERVICE_ACCOUNT = os.getenv("GCP_client_email")
DB_SHEET_ID = os.getenv("DB_SHEET_ID")
DATA_UPLOAD_WORKSHEET_ID = 0


SHEET_DB_CRED_JSON_PATH = CREDENTIALS_DIR / GOOGLE_CREDS_FILE
