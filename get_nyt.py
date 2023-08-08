from dotenv import load_dotenv
import unicodedata
import os
import re
import requests
import pandas as pd
import time

def makedict(x):
    '''
    Takes in a collection of strings and turns it into a dictionary of word counts
    '''
    d = {}
    for item in x:
        # Clean up text - remove punctuation, accents, and contractions.
        item = unicodedata.normalize('NFKD', item)
        item = re.sub('[\'\’\‘\"\“\”]re', '', item)
        item = re.sub('[\'\’\‘\"\“\”]ll', '', item)
        item = re.sub('[\'\’\‘\"\“\”]s', '', item)
        item = re.sub('n[\'\’\‘\"\“\”]t', '', item)
        # A little surprised that splitting on non-word characters decreases the total number of words.  Most must be hyphenated...
        item = re.sub('\W', ' ', item)
        for word in item.lower().split():
            d[word] = d.get(word, 0) + 1
    return d


def get_nyt(m_start,y_start,m_end,y_end):
    '''
    Returns a DataFrame containing a word count dictionary for each day from the NYT data from m_start-y_start (inclusive) to m_end-y_end (exclusive).  If the file is stored locally - it is use.  Otherwise, it is downloaded and saved.
    '''
    load_dotenv()
    key_nyt=os.getenv("NYT_KEY")
    day_data=pd.DataFrame()
    year = y_start
    month = m_start
    while year != y_end or month != m_end:
        csv='data/archive_{:4d}_{:02d}.csv'.format(year,month)

        if os.path.exists(csv):
            df=pd.read_csv(csv,index_col=0,lineterminator='\n')
        else:
            link="https://api.nytimes.com/svc/archive/v1/{:d}/{:d}.json?api-key=".format(year,month)+key_nyt
            r = requests.get(link)
            if r.status_code != 200:
                raise ValueError("Problem accessing NYT\nSTATUS CODE:  {:d}".format(r.status_code))
            r = r.json()['response']['docs']
            df=pd.DataFrame(pd.json_normalize(r))
            df.to_csv(csv)
            time.sleep(12) # as suggested/required in the API documentation

        #convert pub_date to datetime
        df = df.dropna(subset=['pub_date'])
        df['pub_date'] = pd.to_datetime(df['pub_date'],format='mixed')

        df['words'] = df.apply(lambda x:str(x['abstract'])+' '+str(x['lead_paragraph'])+' '+str(x['headline.main']),axis=1)

        day_data = day_data._append(df.groupby(df['pub_date'].dt.date)[['words']].agg(makedict))

        month += 1
        if month == 13:
            month = 1
            year += 1

    return day_data
