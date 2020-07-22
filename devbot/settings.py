from os import environ
from dotenv import load_dotenv

load_dotenv(".env")

DEVBOT_PORT = environ.get("DEVBOT_PORT") if environ.get("DEVBOT_PORT") else 5000
SLACK_TOKEN = environ.get("SLACK_TOKEN")
GATEKEEPER_INTEGRATION_SECRET = environ.get("GATEKEEPER_INTEGRATION_SECRET")
OBOS_URL = environ.get("OBOS_URL")