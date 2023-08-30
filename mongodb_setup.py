import os
import requests
import time
import urllib

from dotenv import load_dotenv
import pandas as pd
import pymongo

# Range of months to store in MongoDB
y_start = 2018
m_start = 1
y_end = 2023
m_end = 8

load_dotenv()
key_nyt = os.getenv("NYT_KEY")
mongo_link = f"mongodb+srv://{os.getenv('MONGODB_USER')}:{os.getenv('MONGODB_USER_PASSWORD')}@{os.getenv('MONGODB_CLUSTER')}?retryWrites=true&w=majority"
mongodb = pymongo.MongoClient(mongo_link)
db = mongodb["nyt_article_summaries"]
mongo_collection = db["articles"]

# Loop over months
year = y_start
month = m_start
while year != y_end or month != m_end:
    date_str = f"{year}_{month:02d}"
    print(date_str)
    # First - save full data from NYT locally
    csv = "data/archive_{:4d}_{:02d}.csv".format(year, month)
    if os.path.exists(csv):
        print("  Data already downloaded.")
        df = pd.read_csv(csv, index_col=0, lineterminator="\n")
    else:
        print("  Downloading data.")
        link = f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={key_nyt}"
        r = requests.get(link)
        if r.status_code != 200:
            raise urllib.error.URLError(
                f"Problem accessing NYT\nSTATUS CODE:  {r.status_code}"
            )
        r = r.json()["response"]["docs"]
        df = pd.DataFrame(pd.json_normalize(r))
        df.to_csv(csv)
        time.sleep(12)  # as suggested/required in the API documentation

    # Next - save relevant data into MongoDB
    response = mongo_collection.find_one(
        {"month": date_str}, projection={"month": True}
    )
    if not response:
        print("  Uploading data")
        articles = df[
            ["pub_date", "abstract", "lead_paragraph", "headline.main", "section_name"]
        ].to_dict(orient="list")
        d = {
            "month": date_str,
            "n_articles": len(articles["pub_date"]),
            "articles": articles,
        }
        mongo_collection.insert_one(d)
    else:
        print("  Data already uploaded")

    # Increment
    month += 1
    if month == 13:
        month = 1
        year += 1
