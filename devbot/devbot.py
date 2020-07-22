import requests
from slack import WebClient
from flask import Flask, request, make_response

app = Flask(__name__)
app.config.from_pyfile("settings.py")

slack_client = WebClient(token=app.config.get("SLACK_TOKEN"))


@app.route("/slack/get-applicants", methods=["POST"])
def command():
    try:
        request_info = request.form
        headers = {
            "Gatekeeper-Integration": app.config.get("GATEKEEPER_INTEGRATION_SECRET")
        }
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


if __name__ == "__main__":
    app.run(threaded=True, port=app.config.get("DEVBOT_PORT"))
