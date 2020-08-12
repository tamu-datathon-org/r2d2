import requests
from .devbot import app

def get_applicant_data():
    headers = {
        "Gatekeeper-Integration": app.config.get("GATEKEEPER_INTEGRATION_SECRET")
    }
    return requests.get(
        f"{app.config.get('OBOS_URL')}/application/all", headers=headers)

def get_attended_events_data():
    headers = {
        "Gatekeeper-Integration": app.config.get("GATEKEEPER_INTEGRATION_SECRET")
    }
    return requests.get(
        f"{app.config.get('GATEKEEPER_URL')}/attended", headers=headers)

def is_authorized_request(request):
    if ("gatekeeper-integration" not in request.headers or 
        request.headers["gatekeeper-integration"] != app.config.get("GATEKEEPER_INTEGRATION_SECRET")):
        return False
    return True