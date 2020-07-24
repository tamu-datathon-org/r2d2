import requests
from slack import WebClient
from flask import Flask, request, make_response

app = Flask(__name__)
app.config.from_pyfile("settings.py")

slack_client = WebClient(token=app.config.get("SLACK_TOKEN"))

# ======== HELPERS ===========
def is_authorized_request(request):
    if "gatekeeper-integration" not in request.headers or request.headers["gatekeeper-integration"] != app.config.get("GATEKEEPER_INTEGRATION_SECRET"):
        return False
    return True


# ======== ENDPOINTS ============

@app.route("/slack/get-applicants", methods=["POST"])
def get_applicants_csv():
    request_info = request.form
    headers = {
        "Gatekeeper-Integration": app.config.get("GATEKEEPER_INTEGRATION_SECRET")
    }
    try:
        applicant_data = requests.get(
            f"{app.config.get('OBOS_URL')}/application/all", headers=headers)
        if (applicant_data.status_code != 200):
            raise Exception("Couldn't get applicant data from Obos.")
        slack_client.files_upload(
            channels=request_info["channel_id"],
            content=applicant_data.text,
            filename="applicants.csv",
            initial_comment="Here's the applicant data!",
            title="Applicant Data"
        )
        # Return nothing so slack bot doesn't auto-reply to command.
        return make_response("", 200)
    except Exception as e:
        return make_response(f"Something went wrong, here's what I know: {e}", 200)


@app.route("/slack/log-error", methods=["POST"])
def log_error():
    if not is_authorized_request(request):
        return make_response(f"Invalid Gatekeeper Integration header", 400)
    if "error" not in request.json:
        return make_response(f"Post body must contain error field", 400)
        
    error_msg = request.json["error"]
    source = request.json["source"] if "source" in request.json else ""
    try:
        error_text = f"ERROR [{source}]:\n\n{error_msg}"
        slack_client.chat_postMessage(
            channel=app.config.get("SLACK_ERROR_LOG_CHANNEL_ID"),
            text=error_text
        )
    except Exception as e:
        print(e)
    return make_response("")


if __name__ == "__main__":
    app.run(threaded=True, port=app.config.get("DEVBOT_PORT"))
