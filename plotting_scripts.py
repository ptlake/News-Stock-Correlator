import matplotlib.pyplot as plt
import numpy as np

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
    plt.savefig('NYT_wc.ps')

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
    plt.savefig('NYT_corr_{:02d}.ps'.format(i))

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
    plt.savefig('NYT_pearson_{:02d}.ps'.format(i))
