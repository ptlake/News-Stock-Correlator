[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ptlake-capstone.streamlit.app) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

#News–Stock Correlator

##Summary

Provide tools to search for correlations between the news and stock prices in the last five years.

##Problem Statement

Have you ever wondered if the news could be a predictor for stock prices? This tool allows
small investors to search for correlations between the news of the last five years with stock
prices. A Streamlit App has been created that resources a MongoDB Atlas Database of news
article summaries from the New York Times and compares it to requested stock tickers. Choose
a date range and a stock ticker to find words that correlate with good/bad days for that stock
during those dates.

##Project

###The Data

The data is procured from two RESTful APIs. The news database chosen is the New
York Times(NYT), as provided by https://developer.nytimes.com/apis. NYT was chosen for both
its general respect in the media and for the fact that the data is provided free of charge at the
time of the creation of this work. The “Archive” endpoint in particular provides information about
every news article published since 1851. The relevant keys used for this work are "pub_date",
"abstract", "lead_paragraph", and "headline.main".
Alpha Vantage provides daily historical stock prices of the last 20+ years free of charge
at https://www.alphavantage.co/. The “TIME_SERIES_DAILY” endpoint provides this
information. The keys from the response used for this work are “timestamp”, “1. open”, and “4.
close”. Alpha Vantage also provides a complete list of tickers that are supported at the
“LISTING_STATUS” endpoint.

###The MongoDB Atlas Database

The MongoDB Atlas Database allows for quick access of the NYT historical data. The
NYT API provides the historical data in one month chunks, but limits the number of calls that
can be made to 5/minute. For the purpose of making an application that can be called on the
fly, the data must be stored somewhere that can promise quicker access to the data. A NoSQL
database is chosen to host the data due to its unstructured nature, and MongoDB Atlas
provides this service for free. The raw data from the NYT API is cleaned and converted to a
CSV file using pandas, keeping only the needed data for the project in the database. The files
are collected in month chunks to keep it similar to the raw source and to limit the number of calls
to the MongoDB for the application. The Python script used to generate the database is found
in the GitHub repository as `mongodb_setup.py` for anyone that would like to create their own
database or extend the scope of the work presented here.

###The Model

The Pearson correlation of daily change in stock prices to word frequency by day is used
as an initial demonstration of how this data can be used. For this purpose, the NYT data set is
merged with the stock data set using pandas. Each word is treated independently of all other
words and the daily change in stock prices is treated as the difference between opening and
closing prices for a given day. To help with the noise due to infrequent words and auxiliary
variable is added to the model to control the minimum number of days the word was found in
the dataset. The top correlated and anti-correlated words are displayed in a Word Cloud.
This first approach to the problem is in general too naive to find any significant
correlations of use in the data, but is a proof of concept of how the framework presented here
can be used. Ideas of models that could be applied to the data include using Word2Vec to get
some correlation in the different words and to consider the time correlation over a few days to
measure any delayed responses.

###The Streamlit Application

The Streamlit application collects all the above ideas into an interactive program that a
user can explore. The input needed is a stock ticker, a date range, and the minimum number of
days that the word needed to be found in the dataset. The program then generates the stock
history for the date range, both with the absolute price and the daily change in price. The
correlation with the historical news data is presented in two plots. One plot shows the Pearson
correlation of each word in increasing order. This data is also shown as a histogram on a
logarithmic scale. If the word frequency is uncorrelated in time, and thus uncorrelated with the
stock price, then all the data will fall in a normal distribution. A Gaussian with the variance of
the observed Pearson correlations is added to this plot to reveal any significant deviations. To
provide further insight to the results two Word Clouds are made to show the most correlated and
anti-correlated words, respectively.

##Deliverables

Github:
https://github.com/ptlake/News-Stock-Correlator

Streamlit:
https://ptlake-capstone.streamlit.app/



