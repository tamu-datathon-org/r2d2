from io import StringIO
import pandas as pd
import json
import time
from ast import literal_eval
from collections import defaultdict

from ..devbot import app
from ..utils import get_applicant_data, is_authorized_request

GENDER_MAP = {
    "F": "Female",
    "M": "Male"
}

CLASSIFICATION_MAP = {
    "Fr": "Freshman",
    "So": "Sophomore",
    "Jr": "Junior",
    "Sr": "Senior",
    "Ma": "Masters",
    "PhD": "PhD",
    "O": "Other"
}

def update_stats_file():
    try:
        applicant_data = get_applicant_data()
        if (applicant_data.status_code != 200):
            return
        data = StringIO(applicant_data.text)
        df = pd.read_csv(data)

        stats = compute_stats(df)
        with open(app.config.get("STATS_FILE"), "w+") as fp:
            json.dump(stats, fp)

    except Exception as e:
        print(e)


def compute_stats(df):
    majors, races, schools, locations, genders, classifications = defaultdict(int), defaultdict(
        int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)
    for i, row in df.iterrows():
        for major in literal_eval(row["majors"]):
            majors[major] += 1
        for race in row["race"].split(", "):
            races[race] += 1
        schools[row["school"]] += 1
        locations[row["physical_location"]] += 1
        if row["gender"] in GENDER_MAP:
            genders[GENDER_MAP[row["gender"]]] += 1
        if row["classification"] in CLASSIFICATION_MAP:
            classifications[CLASSIFICATION_MAP[row["classification"]]] += 1 
    return {
        "timestamp": time.time(),
        "num_apps": len(df),
        "first_gen": len(df[df["first_generation"] == True]),
        "majors": majors,
        "races": races,
        "schools": schools,
        "locations": locations,
        "genders": genders,
        "classifications": classifications
    }
