from dotenv import load_dotenv
import os
import requests
import pandas as pd

def get_stock(stock):
    '''
    Pass in the string `stock` and return the complete history of the stock.
    '''
    csv = 'data/stock_' + stock + '.csv'
    if not os.path.exists(csv):
        load_dotenv()
        key_alv = os.getenv("ALV_KEY")
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stock + '&apikey=' + key_alv + '&outputsize=full'
        r = requests.get(url)
        if r.status_code != 200:
            raise ValueError("Problem accessing Alpha Vantage\nSTATUS CODE:  {:d}".format(r.status_code))
        r = r.json()
        df = pd.DataFrame.from_dict(r['Time Series (Daily)'], orient='index')
        df.to_csv(csv)
    df = pd.read_csv(csv,index_col=0)
    df.index = pd.to_datetime(df.index,format='mixed')
    return df
