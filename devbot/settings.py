from os import environ
from dotenv import load_dotenv

load_dotenv("./devbot/.env")

DEVBOT_PORT = environ.get("DEVBOT_PORT") if environ.get("DEVBOT_PORT") else 5000
SLACK_TOKEN = environ.get("SLACK_TOKEN")
GATEKEEPER_INTEGRATION_SECRET = environ.get("GATEKEEPER_INTEGRATION_SECRET")
OBOS_URL = environ.get("OBOS_URL")
GATEKEEPER_URL = environ.get("GATEKEEPER_URL")
SLACK_ERROR_LOG_CHANNEL_ID = environ.get("SLACK_ERROR_LOG_CHANNEL_ID")

DATA_FILE="data.csv"
STATS_FILE="stats.json"
STATS_UPDATE_FREQUENCY = 600 # in seconds