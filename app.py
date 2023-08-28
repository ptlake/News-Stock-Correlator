from   collections import Counter
from   datetime import datetime, timedelta

import numpy as np
import pandas as pd
from   sklearn.base import BaseEstimator,TransformerMixin
from   sklearn.compose import ColumnTransformer
from   sklearn.feature_extraction import DictVectorizer
from   sklearn.pipeline import Pipeline
import streamlit as st

from   get_nyt import get_nyt
from   get_stock import get_stock
from   plotting_scripts import plot_stock_corr

@st.cache_data
def get_nyt():
    # get the NYT data
    print("Grabbing NYT data...")
    day_data = get_nyt(1, 2021, 7, 2023)
    return day_data

@st.cache_data
def get_stock_names():
    listings = pd.read_csv('listing_status.csv')
    listings['symbol-name'] = listings['symbol'] + ':  ' +  listings['name']
    return listings

@st.cache_data
def get_dates():
    min_date = datetime(2020,1,1)
    max_date = datetime.now()
    return min_date, max_date    

stock_names = get_stock_names()['symbol-name']
min_date,max_date = get_dates()

endash = u'\u2013'
st.title(f"Stock{endash}News Correlator")

with st.form("selections"):
    with st.sidebar:
        stock = st.selectbox('Stock',stock_names)
        month_range = st.slider(
            'Date Range',
            min_value=min_date,
            max_value=max_date,
            value=(min_date,max_date),
            step=timedelta(weeks=1),
            format="MM/YYYY",
        )
        #start_month = month_range[0].strftime('%m/%Y')
        #end_month = month_range[1].strftime('%m/%Y')
        
        submitted = st.form_submit_button("Calculate")
    if submitted:
        st.write(f"Stock -  {stock}")
        st.write(f"Start Date -  {month_range[0].strftime('%m/%Y')}")
        st.write(f"End Date -  {month_range[1].strftime('%m/%Y')}")
    else:
        st.write("Enter a query in the sidebar")

