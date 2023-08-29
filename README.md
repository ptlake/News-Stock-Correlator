# News-Stock Correlator

This streamlit app takes a stock and correlates the daily performance to the words found in the article summaries of the New York Times for that day.  It then displays the daily price change of the stock and the corresponding Pearson correlation to the words found in the paper.  The top 100 positive/negative word correlators are shown in a WordCloud.

The app resources a MongoDB Atlas database I have developed.  It also uses the NYT API to source the current news and AlphaVantage API for stock price history.

Future work will include looking up the current news to determine if recent news suggests an increase or decrease in the stock price.



