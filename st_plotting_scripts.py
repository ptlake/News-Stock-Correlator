from   io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from   wordcloud import WordCloud

def plot_wc(dl):
    plt.rcParams["font.family"] = "Times New Roman"
    fig,ax = plt.subplots(figsize=(6,4))
    ax.set_title("Count frequency, ordered")
    ax.set_ylabel("Count")
    ax.set_xlabel("Index")
    ax.grid()
    ax.set_yscale('log')
    ax.set_xscale('log')
    #ax.set_xticks(np.arange(-1,8),["0.1","1","10","10$^2$","10$^3$","10$^4$","10$^5$","10$^6$","10$^7$"])
    #ax.axis([-1,7,0,225])
    ax.set_axisbelow(True)
    ax.plot(range(len(dl)),dl[ii],linewidth=2,color='black')
    plt.savefig('figs/NYT_wc.ps')

def plot_corr(dl,ii,i):
    plt.rcParams["font.family"] = "Times New Roman"
    fig,ax = plt.subplots(figsize=(6,4))
    ax.set_title("Pearson correlation with given word")
    ax.set_ylabel("Pearson Correlation")
    ax.set_xlabel("Index")
    ax.grid()
    #ax.set_xticks(np.arange(-1,8),["0.1","1","10","10$^2$","10$^3$","10$^4$","10$^5$","10$^6$","10$^7$"])
    ax.axis([0,1000,-1,1])
    ax.set_axisbelow(True)
#    ax.plot(range(len(dl)),[x[ii] for x in dl],linewidth=2,color='black')
    ax.plot(range(len(dl)),dl[ii],linewidth=2,color='black')
    plt.savefig('figs/NYT_corr_{:02d}.ps'.format(i))

def plot_pearson(dl,i):
    plt.rcParams["font.family"] = "Times New Roman"
    fig,ax = plt.subplots(figsize=(8,8))
    ax.set_title("Pearson Correlation")
    ax.set_ylabel("Index")
    ax.set_xlabel("Index")
    ax.grid()
    #ax.set_xticks(np.arange(-1,8),["0.1","1","10","10$^2$","10$^3$","10$^4$","10$^5$","10$^6$","10$^7$"])
    #ax.axis([-1,7,0,225])
    ax.set_axisbelow(True)
    a=ax.imshow(dl,cmap='seismic',vmin=-1,vmax=1,interpolation='none')
    fig.colorbar(a,ax=ax)
    plt.savefig('figs/NYT_pearson_{:02d}.ps'.format(i))

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
