import pandas as pd
from collections import Counter
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from get_stock import get_stock
from get_nyt import get_nyt
from plotting_scripts import plot_stock_corr

class DictTrim(BaseEstimator,TransformerMixin):
    def __init__(self,wlist):
        self.wlist = wlist
    def fit(self, X, y = None):
        return self
    def transform(self, X):
        return [{a:row[a] for a in row.keys() if a in self.wlist} for row in X]

# get the NYT data
print("Grabbing NYT data...")
day_data = get_nyt(1, 2022, 7, 2023)
#day_data = get_nyt(4, 2023, 7, 2023)

# get the stock data
print("Grabbing stock data...")
stock_data = get_stock("IBM")
stock_data['diff'] = stock_data['4. close'] - stock_data['1. open']

# merge NYT and stock
day_data = day_data.merge(stock_data['diff'], how='left', left_index=True, right_index=True)
day_data = day_data.dropna(subset=['diff'])

selector = ColumnTransformer([('word_vectorizer',DictVectorizer(sparse=False),'words')])

v = selector.fit_transform(day_data)

avg_word = v.mean(0)
var_word = v.var(axis=0,ddof=0)

avg_stock = day_data['diff'].mean()
var_stock = day_data['diff'].var(ddof=0)

pearson = (np.dot(v.T,day_data['diff'])/len(v)-avg_stock*avg_word)/np.sqrt(var_stock*var_word)
plot_stock_corr(pearson)
'''
d=Counter()
for y in day_data['words']:
    d.update(y)
print(len(d))
dl=sorted(list(d.items()),key=lambda x:x[1],reverse=True)
print(len(day_data))

wlist=tuple(x[0] for x in d.most_common(1000))


#w=DictTrim(wlist)
#v=DictVectorizer(sparse=False)
#d2=w.fit_transform(day_data['words'])
#mat=v.fit_transform(d2)

v=DictVectorizer(sparse=False)
mat=v.fit_transform(day_data['words'])


#normalize rows to remove fluctuations due to total words per day
mat/=np.sum(mat,axis=1)[:,None]

#from sklearn.cluster import KMeans
#kmeans=KMeans(n_clusters=1000).fit(mat)

from sklearn.decomposition import PCA

pca=PCA(n_components=546).fit(mat)
cumsum=0
for i,a in enumerate(pca.explained_variance_ratio_):
    cumsum+=a
    print(i,a,cumsum)

#plot_wc(dl)
'''



'''
# Time correlations
for i in range(15):
    if i==0:
        pearson=(mat.T.dot(mat))
        pearson/=len(mat)
        pearson-=np.sum(mat,axis=0)[:,None]*np.sum(mat,axis=0)[None,:]/len(mat)**2
        std1=np.sqrt(np.diag(pearson))
        std2=std1.copy()
    else:
        pearson=(mat[i:].T.dot(mat[:-i]))
        pearson/=len(mat)-i
        pearson-=np.sum(mat[i:],axis=0)[:,None]*np.sum(mat[:-i],axis=0)[None,:]/(len(mat)-i)**2
        std1=np.sqrt(np.sum(mat[ i:]**2,axis=0)/(len(mat)-i)-np.sum(mat[ i:],axis=0)**2/(len(mat)-i)**2)
        std2=np.sqrt(np.sum(mat[:-i]**2,axis=0)/(len(mat)-i)-np.sum(mat[:-i],axis=0)**2/(len(mat)-i)**2)
    pearson/=std1[:,None]*std2[None,:]
    plot_pearson(pearson,i)
    print(np.max(np.diag(pearson)),np.min(np.diag(pearson)))
    print(np.max(pearson),np.min(pearson))
    
    
    plot_corr(pearson,v.vocabulary_['ukraine'],i)

    ii=v.vocabulary_['ukraine']
    for i,a in enumerate(pearson[ii]):
        if a>0.25 or a<-0.25:
            print(v.feature_names_[i],a)
    print("")
'''
#print(wlist)

