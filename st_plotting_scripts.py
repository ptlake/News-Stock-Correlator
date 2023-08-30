import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from wordcloud import WordCloud


def plot_stock_corr(y):
    # plt.rcParams["font.family"] = "Times New Roman"
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_title("Pearson correlation with each word, increasing")
    ax.set_ylabel("Pearson Correlation")
    ax.set_xlabel("Ordered Ranking")
    ax.grid()
    ax.set_axisbelow(True)
    ax.plot(range(len(y)), y, linewidth=2, color="black")
    ax.axis([0, len(y), -1, 1])
    st.pyplot(fig)


def plot_stock_corr_hist(y):
    # plt.rcParams["font.family"] = "Times New Roman"
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_title("Frequency of Pearson correlation with each word")
    ax.set_ylabel("Count")
    ax.set_xlabel("Pearson Correlation")
    ax.set_yscale("log")
    ax.grid()
    ax.set_axisbelow(True)

    maxy = max(np.abs(y))
    dx = maxy / 10.0
    bins = np.arange(-10 * dx, 10 * dx, dx)
    x = np.arange(-maxy, maxy, 0.01)
    sig2 = np.var(y)
    gauss = dx * np.exp(-(x**2) / 2.0 / sig2) * len(y) / np.sqrt(2 * np.pi * sig2)

    ax.hist(
        y, linewidth=2, bins=bins, density=False, edgecolor="black", color="#777777"
    )
    ax.plot(x, gauss)
    ax.set_ylim(bottom=0.1, auto=True)
    st.pyplot(fig)


def plot_stock(y, month_range):
    # plt.rcParams["font.family"] = "Times New Roman"
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_title("Daily stock price at close")
    ax.set_ylabel("price (USD)")
    ax.set_xlabel("Date")
    ax.grid()
    ax.set_xlim(month_range)
    ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_axisbelow(True)
    ax.plot(y.index, y["4. close"], linewidth=2, color="black")
    st.pyplot(fig)


def plot_stock_diff(y, month_range):
    # plt.rcParams["font.family"] = "Times New Roman"
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_title("Daily stock price change")
    ax.set_ylabel("$\Delta$ price (USD)")
    ax.set_xlabel("Date")
    ax.grid()
    ax.set_xlim(month_range)
    ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_axisbelow(True)
    ax.plot(y.index, y["diff"], linewidth=2, color="black")
    st.pyplot(fig)


def positive_words(words):
    wordcloud = WordCloud(colormap="Greens").generate_from_frequencies(words)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(fig)


def negative_words(words):
    wordcloud = WordCloud(colormap="Oranges").generate_from_frequencies(words)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(fig)
