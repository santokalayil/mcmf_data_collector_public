from .web_processor import app
from .paths import GCP_CREDENTIALS_JSON_PATH
from .utils import create_gcp_credentials_json

def main_interface():
    if not GCP_CREDENTIALS_JSON_PATH.is_file():
        create_gcp_credentials_json()

    app.render()


