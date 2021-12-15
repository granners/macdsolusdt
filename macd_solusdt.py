import json
import pandas as pd
import requests
from datetime import datetime
import pandas
import io
import stockstats
import matplotlib.pyplot as plt
import pandas as pd

from_symbol = 'SOL'
to_symbol = 'USD'
exchange = 'CryptoCompare/CCCAGG'
datetime_interval = 'day'

#Download data
def download_data(from_symbol,to_symbol,exchange,datetime_interval):
        # def get_data():
        print(f"Downloading {from_symbol} to {to_symbol} data from the crypto compare api...")
        url = 'https://min-api.cryptocompare.com/data/v2/histoday?fsym=SOL&tsym=USD&limit=1000&aggregate=1&e=CCCAGG'
        #url = 'https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=2000&aggregate=1'
        new_url = requests.get(url,datetime_interval)
        # print(new_url)
        r = requests.get(url)
        data = r.json()
        return data

#Convert to pandas date frame
#Data has to be in a list format to use pandas.
def convert_to_list(data):
        d_1 = data['Data']
        d_2 = d_1['Data']
        data_list = list(d_2)
        # d_type = type(data_list)
        # df = pd.DataFrame(data_list)
        # df['datetime'] = pd.to_datetime(df.time, unit='s')
        #
        # print(df)
        return data_list
#convert to DF

def convert_to_data_frame(data_list):
        df = pd.json_normalize(data_list)
        df['datetime'] = pd.to_datetime(df.time, unit='s')
        df = df[['datetime', 'low', 'high', 'open',
        'close', 'volumefrom', 'volumeto']]
        return df

#filtering empty data points
def filtering_empty_data_points(df):
        indices = df[df.sum(axis=1) == 0].index
        print('Filtering %d empty datapoints' % indices.shape[0])
        df = df.drop(indices)
        # print(df)
        return df
#find the macd using stockstats '''LAZY'''
def finding_macd(df):
        df = stockstats.StockDataFrame(df)
        df['macd'] = df.get('macd')
        return(df)

data = download_data(from_symbol,to_symbol,exchange,datetime_interval)
list = convert_to_list(data)
df = convert_to_data_frame(list)
df = filtering_empty_data_points(df)
df = finding_macd(df)

#plotting the graph using matplotlib
df.plot(kind='bar',x='datetime',y='macd',color='green')
plt.show()
