from io import StringIO
import pandas as pd
import json
import time

from ..devbot import app
from ..utils import get_applicant_data, is_authorized_request


def update_stats_file():
    try:
        applicant_data = get_applicant_data()
        if (applicant_data.status_code != 200):
            return
        data = StringIO(applicant_data.text)
        df = pd.read_csv(data)

        # Compute stats
        stats = {}
        stats["timestamp"] = time.time()
        stats["num_applications"] = df.shape[0]

        with open(app.config.get("STATS_FILE"), "w+") as fp:
            json.dump(stats, fp)

    except Exception as e:
        print(e)


def format_stats_for_message(data):
    return f"""
    ```
    Number of applicants: {data["num_applications"]}
    ```
    """