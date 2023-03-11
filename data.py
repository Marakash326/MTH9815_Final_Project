import pandas as pd
import datetime
import os


def Process(data: pd.DataFrame) -> pd.DataFrame:
    def calTarget(x):
        x = x.sort_values(by='Date')
        x['target'] = (x['CumReturnResid_15:30'].shift(-1)+1)*((x['CumReturnResid_16:00']+1)/(x['CumReturnResid_15:30']+1))-1
        return x
    
    data = data.groupby(by='Id').apply(calTarget)
    return data


def IntradayData(inputDir: str, compressDir: str, compress: bool=True) -> pd.DataFrame:
    if compress:
        df_lst = []
        for file in os.listdir(inputDir):
            df_lst.append(pd.read_csv(inputDir + '/' + file))
        df = pd.concat(df_lst)
        df = df.pivot(index=['Date', 'Id'], columns='Time', values=['CumReturnResid', 'CumReturnRaw', 'CumVolume'])
        df = df.reset_index()
        columns = df.columns
        columns = ['Date', 'Id'] + [s[0] + '_' + s[1][:5] for s in columns[2:28]] + [s[0] + '_' + s[1][:5] for s in columns[28:54]] +[s[0] + '_' + s[1][:5] for s in columns[54:90]]
        df.columns = columns
        df = df.sort_values(by='Date').reset_index(drop=True)
        df.to_csv(compressDir + '/intraday.csv',index=False)
        return df
    
    else:
        dateDf = pd.read_csv('intraday.csv')
        return dateDf
        


def DailyData(inputDir: str, read: bool = True)->pd.DataFrame:
    if read:
        dailyData = pd.read_csv('dailyProcessed.csv')
        col = dailyData.columns.values
        col[1] = 'Id'
        dailyData.columns = col
    else:
        dailyData = []
        for root,dir,files in os.walk('daily_data'):
            for f in files:
                dailyData.append(pd.read_csv(os.path.join(root,f)))
        dailyData = pd.concat(dailyData)
        dailyData = dailyData.sort_values(by='Date').reset_index(drop=True)
        col = dailyData.columns.values
        col[1] = 'Id'
        dailyData.columns = col
    return dailyData


def Data(inputDir: str, startDate: datetime.date, endDate: datetime.date)->pd.DataFrame:

    # intradayDf = IntradayData('intraday_data', 'compress/', False)
    # dailyDf = DailyData('daily_data')
    # data = intradayDf.merge(dailyDf,on=['Date','Id'])

    # data = Process(data)
    data = pd.read_csv("raw.csv")

    startDateInt = int(startDate.strftime('%Y%m%d'))
    endDateInt = int(endDate.strftime('%Y%m%d'))
    data = data[data['Date']>=startDateInt]
    data = data[data['Date']<=endDateInt]

    return data


# def IntradayData(inputDir: str, compressDir: str, compress: bool=True) -> pd.DataFrame:
#     if compress:
#         dateDf = []
#         timestamps = ['09:45:00.000','10:00:00.000','10:15:00.000',
#         '10:30:00.000','10:45:00.000','11:00:00.000','11:15:00.000',
#         '11:30:00.000','11:45:00.000','12:00:00.000','12:15:00.000',
#         '12:30:00.000','12:45:00.000','13:00:00.000','13:15:00.000',
#         '13:30:00.000','13:45:00.000','14:00:00.000','14:15:00.000',
#         '14:30:00.000','14:45:00.000','15:00:00.000','15:15:00.000',
#         '15:30:00.000','15:45:00.000','16:00:00.000']
#         suffix = [i[:5] for i in timestamps]
#         features = ['CumReturnResid','CumReturnRaw','CumVolume']
#         cols = [j+'_'+i for i in suffix for j in features ]
#         cols = cols

#         cnt = 0
#         for root, dirs, files in os.walk(inputDir):
#             for file in files:
#                 print('*',end='')
#                 cnt+=1
#                 if cnt%10 == 0:
#                     print(' ', end='')
#                 if cnt%100 == 0:
#                     print()
#                 df = pd.read_csv(os.path.join(root, file))

#                 def compress(x):
#                     templist = []
#                     tempdf = x[['Time','CumReturnResid','CumReturnRaw','CumVolume']].set_index('Time')
#                     for i in range(len(timestamps)):
#                         for j in range(len(features)):
#                             templist.append(tempdf.loc[timestamps[i],features[j]])
#                     return pd.DataFrame([templist],columns=cols)

#                 newdf = df.groupby('Id').apply(compress)
#                 newdf = newdf.reset_index(drop=False)
#                 newdf['Date'] = df.loc[0,'Date']
#                 newdf = newdf[['Date','Id']+cols]
#                 dateDf.append(newdf)
#                 newdf.to_csv(os.path.join(compressDir,file),index=False)
#         dateDf = pd.concat(dateDf,axis=0)
#         dateDf = dateDf.sort_values(by='Date').reset_index(drop=True)
#         dateDf.to_pickle('raw.pkl')
#         return dateDf
    
#     else:
#         dateDf = pd.read_csv('raw.csv')
#         return dateDf