import json
from slack import WebClient
from flask import Flask, request, make_response
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config.from_pyfile("settings.py")

# Utils use app, import it after initializing
from .utils import get_applicant_data, is_authorized_request, get_attended_events_data
from .stats import format_stats_for_message, update_stats_file

slack_client = WebClient(token=app.config.get("SLACK_TOKEN"))

# Start background process to update stats file intermittently.
update_stats_file()
scheduler = BackgroundScheduler()
scheduler.add_job(update_stats_file, 'interval', seconds=app.config.get("STATS_UPDATE_FREQUENCY"))
scheduler.start()

# ======== ENDPOINTS ============

@app.route("/slack/get-applicants", methods=["POST"])
def get_applicants_csv():
    request_info = request.form
    try:
        applicant_data = get_applicant_data()
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

@app.route("/slack/get-applicant-stats", methods=["POST"])
def get_applicantion_stats():
    request_info = request.form
    try:
        data = None
        with open(app.config.get("STATS_FILE"), "r") as fp:
            data = json.load(fp)
        if not data:
            return make_response(f"I'm still loading the stats, please try after some time :)", 200)
        
        msg = f"Application Statistics:{format_stats_for_message(data)}"
        slack_client.chat_postMessage(
            channel=request_info["channel_id"],
            text=msg
        )

    except Exception as e:
        return make_response(f"Something went wrong, here's what I know: {e}", 200)
    return make_response("")

@app.route("/slack/attended-emails", methods=["POST"])
def get_attended_emails():
    request_info = request.form
    try:
        user_msg = request_info.get('text')
        event_id = user_msg[user_msg.find('eventId') + len('eventId '):]
        attended_events_data = get_attended_events_data(event_id)
        data = list(attended_events_data.json())

        msg = 'timestamp,authId,email'
        for d in data:
            msg += '\n' + d['timestamp'] + ',' + d['userAuthId'] + ',' + d['userEmail']

        slack_client.files_upload(
            channels=request_info["channel_id"],
            content=msg,
            filename="event_attended_emails.csv",
            initial_comment=f"Here are the participants who attended event {event_id}",
            title="Event Attended Emails"
        )

    except Exception as e:
        return make_response(f"Something went wrong, here's what I know: {e}", 200)
    return make_response("")

@app.route("/slack/log-error", methods=["POST"])
def log_error():
    if not is_authorized_request(request):
        return make_response(f"Invalid Gatekeeper Integration header", 400)
    if "error" not in request.json:
        return make_response(f"Post body must contain error field", 400)
        
    error_msg = request.json["error"]
    source = request.json["source"] if "source" in request.json else ""
    try:
        error_text = f"Error [{source}]:```{error_msg}```"
        slack_client.chat_postMessage(
            channel=app.config.get("SLACK_ERROR_LOG_CHANNEL_ID"),
            text=error_text
        )

    except Exception as e:
        print(e)
    return make_response("")


if __name__ == "__main__":
    app.run(threaded=True, port=app.config.get("DEVBOT_PORT"))
