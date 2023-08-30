from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pymongo

from sklearn.feature_extraction.text import CountVectorizer
import streamlit as st

from st_get_nyt import get_nyt
from st_get_stock import get_stock
import st_plotting_scripts


@st.cache_data
def init_nyt():
    # get the NYT data
    mongo_link = f"mongodb+srv://{st.secrets['MONGODB_USER']}:{st.secrets['MONGODB_USER_PASSWORD']}@{st.secrets['MONGODB_CLUSTER']}?retryWrites=true&w=majority"
    mongodb = pymongo.MongoClient(mongo_link)
    db = mongodb["nyt_article_summaries"]
    mongo_collection = db["articles"]
    # print("Grabbing NYT data...")
    day_data = get_nyt(mongo_collection, 1, 2018, 8, 2023)
    return day_data


@st.cache_data
def get_stock_names():
    listings = pd.read_csv("listing_status.csv")
    listings["symbol-name"] = listings["symbol"] + " - " + listings["name"]
    placeholder = pd.DataFrame({"symbol-name": "<select stock ticker>"}, index=[0])
    listings = pd.concat([placeholder, listings]).reset_index(drop=True)
    return listings


@st.cache_data
def get_dates():
    min_date = datetime(2018, 1, 1)
    max_date = datetime.now()
    return min_date, max_date


min_date, max_date = get_dates()
stock_names = get_stock_names()

endash = "\u2013"
st.title(f"News{endash}Stock Correlator")

day_data = init_nyt()

with st.form("selections"):
    with st.sidebar:
        stock_index = st.selectbox(
            "Stock",
            range(len(stock_names)),
            format_func=lambda x: stock_names["symbol-name"][x],
        )
        month_range = st.slider(
            "Date Range",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            step=timedelta(weeks=1),
            format="MM/YYYY",
        )
        word_freq = st.slider(
            "Minumum Word Frequency", min_value=5, max_value=100, step=1
        )
        submitted = st.form_submit_button("Calculate")

    if not submitted:
        st.write("Enter a query in the sidebar")
    else:
        stock_name = stock_names["symbol-name"][stock_index]
        st.write(f"Stock:  {stock_name}")
        st.write(
            f"Date Range:\
                  {month_range[0].strftime('%m/%Y')}\
                  - {month_range[1].strftime('%m/%Y')}"
        )
        st.write(f"Minimum Word Frequency: {word_freq}")
        st.markdown("""---""")

        ticker = stock_names.iloc[stock_index]
        if pd.notnull(ticker["symbol"]):
            stock_data = get_stock(ticker["symbol"])
            stock_data["diff"] = stock_data["4. close"] - stock_data["1. open"]

            month_range = [x.replace(day=1).date() for x in month_range]

            stock_day_data = day_data.loc[month_range[0] : month_range[1]].merge(
                stock_data, how="inner", left_index=True, right_index=True
            )

            vectorizer = CountVectorizer(min_df=word_freq)

            v = vectorizer.fit_transform(stock_day_data["words"])
            v = np.array(v.todense())
            features = vectorizer.get_feature_names_out()

            avg_word = v.mean(0)
            var_word = v.var(axis=0, ddof=0)
            avg_stock = (stock_day_data["diff"]).mean()
            var_stock = (stock_day_data["diff"]).var(ddof=0)
            pearson = (
                np.dot(v.T, stock_day_data["diff"]) / len(v) - avg_stock * avg_word
            ) / np.sqrt(var_stock * var_word)

            ind = np.argpartition(pearson, -100)[-100:]
            ind = ind[np.argsort(pearson[ind])]
            positive_weights = {features[i]: pearson[i] for i in ind}
            ind = np.argpartition(pearson, 100)[:100]
            ind = ind[np.argsort(pearson[ind])]
            negative_weights = {features[i]: -pearson[i] for i in ind}

            st.write("Stock History")
            col1, col2 = st.columns(2)
            with col1:
                st_plotting_scripts.plot_stock(stock_day_data, month_range)
            with col2:
                st_plotting_scripts.plot_stock_diff(stock_day_data, month_range)
            st.write("Word Correlation Plots")
            col1, col2 = st.columns(2)
            with col1:
                st_plotting_scripts.plot_stock_corr(sorted(pearson))
            with col2:
                st_plotting_scripts.plot_stock_corr_hist(pearson)
            col1, col2 = st.columns(2)
            with col1:
                st.write("Positive Correlators")
                st_plotting_scripts.positive_words(positive_weights)
            with col2:
                st.write("Negative Correlators")
                st_plotting_scripts.negative_words(negative_weights)
