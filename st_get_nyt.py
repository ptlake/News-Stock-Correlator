import unicodedata
import re

import pandas as pd


def makedict(x):
    """
    Takes in a collection of strings and turns it into a dictionary of word counts
    """
    d = {}
    for item in x:
        # Clean up text - remove punctuation, accents, and contractions.
        item = unicodedata.normalize("NFKD", item)
        item = re.sub("['\’\‘\"\“\”]re", "", item)
        item = re.sub("['\’\‘\"\“\”]ll", "", item)
        item = re.sub("['\’\‘\"\“\”]s", "", item)
        item = re.sub("n['\’\‘\"\“\”]t", "", item)
        # A little surprised that splitting on non-word characters decreases the total number of words.  Most must be hyphenated...
        item = re.sub("\W", " ", item)
        for word in item.lower().split():
            d[word] = d.get(word, 0) + 1
    return d


def clean_string(x):
    """Cleans up strings to be analyzed."""
    x = unicodedata.normalize("NFKD", x)
    x = re.sub("['\’\‘\"\“\”]re", "", x)
    x = re.sub("['\’\‘\"\“\”]ll", "", x)
    x = re.sub("['\’\‘\"\“\”]s", "", x)
    x = re.sub("n['\’\‘\"\“\”]t", "", x)
    # A little surprised that splitting on non-word characters decreases the total number of words.  Most must be hyphenated...
    x = re.sub("\W", " ", x)
    return x


def get_nyt(mongo_collection, m_start, y_start, m_end, y_end):
    """
    Returns a DataFrame containing a word count dictionary for each day from the NYT data from m_start-y_start (inclusive) to m_end-y_end (exclusive).  If the file is stored locally - it is use.  Otherwise, it is downloaded and saved.
    """
    day_data = pd.DataFrame()
    year = y_start
    month = m_start
    while year != y_end or month != m_end:
        date_str = f"{year}_{month:02d}"
        response = mongo_collection.find_one({"month": date_str})
        df = pd.DataFrame.from_dict(response["articles"])

        # convert pub_date to datetime
        df = df.dropna(subset=["pub_date"])
        df["pub_date"] = pd.to_datetime(df["pub_date"], format="mixed")

        # df['words'] = df.apply(lambda x:str(x['abstract'])+' '+str(x['lead_paragraph'])+' '+str(x['headline.main']),axis=1)
        # day_data = day_data._append(df.groupby(df['pub_date'].dt.date)[['words']].agg(makedict))

        df["words"] = df.apply(
            lambda x: clean_string(
                f"{x['abstract']} {x['lead_paragraph']} {x['headline.main']} "
            ),
            axis=1,
        )

        day_data = day_data._append(
            df.groupby(df["pub_date"].dt.date)[["words"]].agg(sum)
        )

        month += 1
        if month == 13:
            month = 1
            year += 1

    return day_data
