import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def IC(data: pd.DataFrame, save: bool):
    # Example:
    # RankIC(df[['Date','Open','target']])
    # 3 columns input, the second one is the feature to be tested

    def rankcorr(x):
        return x.dropna().corr('pearson').values[1,2]
    rankic = data.groupby('Date').apply(rankcorr)
    print(data.columns[1], end='    ')
    print('IC Mean:',rankic.mean(), end='    ')
    print('IC Std:',rankic.std())
    rankic = rankic.reset_index()
    rankic['Date'] = pd.to_datetime(rankic['Date'].astype(str), format='%Y%m%d')
    rankic = rankic.set_index('Date')
    plt.plot(rankic)
    plt.hlines(0,rankic.index[0],rankic.index[-1],color='red',linestyles='dashed')
    if save:
        plt.savefig('pic/'+str(data.columns[1])+'.png')
        plt.close()
    else:
        plt.show()
        plt.close()
        

def RankIC(data: pd.DataFrame, save: bool):
    # Example:
    # RankIC(df[['Date','Open','target']])
    # 3 columns input, the second one is the feature to be tested

    def rankcorr(x):
        return x.dropna().corr('spearman').values[1,2]
    rankic = data.groupby('Date').apply(rankcorr)
    print(data.columns[1], end='    ')
    print('RankIC Mean:',rankic.mean(), end='    ')
    print('RankIC Std:',rankic.std())
    rankic = rankic.reset_index()
    rankic['Date'] = pd.to_datetime(rankic['Date'].astype(str), format='%Y%m%d')
    rankic = rankic.set_index('Date')
    plt.plot(rankic)
    plt.hlines(0,rankic.index[0],rankic.index[-1],color='red',linestyles='dashed')
    if save:
        plt.savefig('pic/'+str(data.columns[1])+'.png')
        plt.close()
    else:
        plt.show()
        plt.close()
        

def Simulate(data: pd.DataFrame, save: bool):
    def longshort(x):
        if not x.dropna().shape[0]:
            return 0
        col = x.columns[1]
        up = x[col].dropna().quantile(0.9)
        low = x[col].dropna().quantile(0.1)
        buy = x[x[col]>=up]
        sell = x[x[col]<=low]
        pctbuy = 1.0/buy.shape[0]
        pctsell = 1.0/sell.shape[0]
        pnl = np.exp(buy['target']).sum()*pctbuy - np.exp(sell['target']).sum()*pctsell
        return pnl

    pnl = data.groupby(by='Date').apply(longshort)
    pnl = pnl.reset_index()
    pnl['Date'] = pd.to_datetime(pnl['Date'].astype(str), format='%Y%m%d')
    pnl = pnl.set_index('Date')

    print('Long Short Simulation:', data.columns[1])
    for i in sorted(list(set(pnl.index.year))):
        ydf = pnl[pnl.index.year==i]
        print(i, (ydf.mean()/ydf.std()*np.sqrt(251)).loc[0])
    print('Total', (pnl.mean()/pnl.std()*np.sqrt(251)).loc[0])

    pnl.cumsum().plot()
    if save:
        plt.savefig('pic/'+str(data.columns[1])+'_pnl.png')
        plt.close()
    else:
        plt.show()
        plt.close()