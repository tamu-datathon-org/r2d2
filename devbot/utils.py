from __main__ import app


def is_authorized_request(request):
    if "gatekeeper-integration" not in request.headers or request.headers["gatekeeper-integration"] != app.config.get("GATEKEEPER_INTEGRATION_SECRET"):
        return False
    return True
