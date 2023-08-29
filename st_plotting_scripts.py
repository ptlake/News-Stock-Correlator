from   io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from   wordcloud import WordCloud


def plot_stock_corr(y):
    plt.rcParams["font.family"] = "Times New Roman"
    fig,ax = plt.subplots(figsize=(6,4))
    ax.set_title("Pearson correlation with each word, increasing")
    ax.set_ylabel("Pearson Correlation")
    ax.set_xlabel("Index")
    ax.grid()
    #ax.set_xticks(np.arange(-1,8),["0.1","1","10","10$^2$","10$^3$","10$^4$","10$^5$","10$^6$","10$^7$"])
    ax.axis([0,len(y),-1,1])
    ax.set_axisbelow(True)
    ax.plot(range(len(y)),y,linewidth=2,color='black')
    st.pyplot(fig)
    #buf = BytesIO()
    #fig.savefig(buf, format="png")
    #st.image(buf)

def plot_stock(y,month_range):
    plt.rcParams["font.family"] = "Times New Roman"
    fig,ax = plt.subplots(figsize=(6,4))
    ax.set_title("Daily stock price change")
    ax.set_ylabel("$\Delta$ price (USD)")
    ax.set_xlabel("Date")
    ax.grid()
    ax.set_xlim(month_range)
    ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(),rotation=45,ha='right')
    ax.set_axisbelow(True)
    ax.plot(y.index,y['diff'],linewidth=2,color='black')
    st.pyplot(fig)
    #buf = BytesIO()
    #fig.savefig(buf, format="png")
    #st.image(buf)

def positive_words(words):
    wordcloud = WordCloud(colormap='Blues').generate_from_frequencies(words)
    fig, ax = plt.subplots(figsize = (12, 8))
    ax.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(fig)

def negative_words(words):
    wordcloud = WordCloud(colormap='Reds').generate_from_frequencies(words)
    fig, ax = plt.subplots(figsize = (12, 8))
    ax.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(fig)
