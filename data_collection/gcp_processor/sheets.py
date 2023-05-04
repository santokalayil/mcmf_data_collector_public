# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import json

# from pathlib import Path
# SHEET_DB_CRED_JSON_PATH = Path("/home/santokalayil/Documents/church/data_collection/assets/credentials/google_sheet_db__datacollector.json")

# SERVICE_ACCOUNT = "google-sheet-db-access@datacollector-380107.iam.gserviceaccount.com"

# # Set the path to the credentials JSON file
# creds_file_path = "path/to/credentials.json"

# # Set the scope of the API client
# scope = ["https://www.googleapis.com/auth/spreadsheets"]

# # Create credentials object from the JSON file
# creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file_path, scope)

# # Authorize the client using the credentials
# client = gspread.authorize(creds)

# # Open the Google Sheet by its URL or ID
# sheet_url = "https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit#gid=SHEET_ID"
# sheet = client.open_by_url(sheet_url).worksheet("Sheet1")

# # Add a new row of data to the sheet
# row_data = ["New Data 1", "New Data 2", "New Data 3"]
# sheet.append_row(row_data)

import gspread

from .cred import SHEET_DB_CRED_JSON_PATH, DB_SHEET_ID, DATA_UPLOAD_WORKSHEET_ID
from ..paths import CONFIGURATION_DIR
from ..config import DB_COLUMNS



def add_record(columns_data):
    global DB_COLUMNS
    gs = gspread.service_account(filename=SHEET_DB_CRED_JSON_PATH)
    wb = gs.open_by_key(DB_SHEET_ID)
    sh = wb.get_worksheet_by_id(id=DATA_UPLOAD_WORKSHEET_ID)
    
    row_in_dict_format = {col: columns_data[col] if col in columns_data.keys() else "" for col in DB_COLUMNS}
    row_in_list_format = list(row_in_dict_format.values())
    sh.append_row(row_in_list_format)


