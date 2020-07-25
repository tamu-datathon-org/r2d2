from io import StringIO
import pandas as pd
import json
import time
from ast import literal_eval
from collections import defaultdict

from ..devbot import app
from ..utils import get_applicant_data, is_authorized_request


def update_stats_file():
    try:
        applicant_data = get_applicant_data()
        if (applicant_data.status_code != 200):
            return
        data = StringIO(applicant_data.text)
        df = pd.read_csv(data)

        # Process complex data
        majors, races, schools = defaultdict(int), defaultdict(int), defaultdict(int)
        for i, row in df.iterrows():
            for major in literal_eval(row["majors"]):
                majors[major] += 1
            for race in row["race"].split(", "):
                races[race] += 1
            schools[row["school"]] += 1

        # Write stats
        stats = {
            "timestamp": time.time(),
            "num_apps": len(df),
            "first_gen": len(df[df["first_generation"] == True]),
            "majors": majors,
            "races": races,
            "schools": schools
        }

        with open(app.config.get("STATS_FILE"), "w+") as fp:
            json.dump(stats, fp)

    except Exception as e:
        print(e)


def format_stats_for_message(stats):
    major_count_list = [(major, stats["majors"][major]) for major in stats["majors"]]
    major_count_list.sort(key=lambda x: x[1], reverse=True)
    top_5_majors = [f"{major} ({int(count / stats['num_apps'] * 100)}%)" for major, count in major_count_list[:5]]

    school_count_list = [(school, stats["schools"][school]) for school in stats["schools"]]
    school_count_list.sort(key=lambda x: x[1], reverse=True)
    top_5_schools = [f"{school} ({int(count / stats['num_apps'] * 100)}%)" for school, count in school_count_list[:5]]

    return f"""
    ```
    ## General Stats:
    Number of applicants: {stats["num_apps"]}
    TAMU Applications: {stats["majors"]["Texas A&M University"]}
    
    ## Education Stats
    First Generation Students: {stats["first_gen"]} ({int(stats["first_gen"]/stats["num_apps"]*100)}%)
    Top 5 Majors: {" |>| ".join(top_5_majors)}
    Top 5 Schools: {" |>|".join(top_5_schools)}
    ```
    """
