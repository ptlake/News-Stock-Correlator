import requests
import urllib

import pandas as pd
import streamlit as st

@st.cache_data
def get_stock(stock):
    '''
    Pass in the string `stock` and return the complete history of the stock.
    '''
    load_dotenv()
    url = 'https://www.alphavantage.co/query'
    r = requests.get(url,
            params={
                'function':'TIME_SERIES_DAILY',
                'symbol': stock,
                'apikey': st.secrets["ALV_KEY"],
                'outputsize':'full'
            })
    if r.status_code != 200:
            raise urllib.error.URLError(f'Problem accessing Alpha Vantage\nSTATUS CODE:  {r.status_code}')
    r = r.json()
    type_dict={
        '1. open': float,
        '2. high': float,
        '3. low': float,
        '4. close': float,
        '5. volume': float
    }
    df = pd.DataFrame.from_dict(r['Time Series (Daily)'], orient='index').astype(type_dict)
    df.index = pd.to_datetime(df.index,format='mixed')
    return df
