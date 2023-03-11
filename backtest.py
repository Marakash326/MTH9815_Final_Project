import pandas as pd
import matplotlib.pyplot as plt

def RankIC(data: pd.DataFrame):
    # Example:
    # RankIC(df[['Date','Open','target']])
    # 3 columns input, the second one is the feature to be tested

    def rankcorr(x):
        return x.dropna().corr('spearman').values[1,2]
    rankic = data.groupby('Date').apply(rankcorr)
    print('RankIC Mean:',rankic.mean())
    print('RankIC Std:',rankic.std())
    rankic = rankic.reset_index()
    rankic['Date'] = pd.to_datetime(rankic['Date'].astype(str), format='%Y%m%d')
    rankic = rankic.set_index('Date')
    plt.plot(rankic)
    plt.hlines(0,rankic.index[0],rankic.index[-1],color='red',linestyles='dashed')
    plt.show()