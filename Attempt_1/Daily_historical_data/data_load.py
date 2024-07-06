from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import numpy as np
import talib as tb
import time
import os
import pywhatkit
import matplotlib.pyplot as plt
from datetime import datetime

tv = TvDatafeed()

n50_symbols=np.array(['NIFTY', 'HINDALCO', 'MARUTI', 'NESTLEIND', 'ONGC', 'TATAMOTORS', 'ITC', 'SUNPHARMA', 'BHARTIARTL', 'CIPLA', 'DIVISLAB', 'JSWSTEEL', 'HINDUNILVR', 'TITAN', 'NTPC', 'TATASTEEL', 'HEROMOTOCO', 'HDFCLIFE', 'ULTRACEMCO', 'SBILIFE', 'TCS', 'BAJFINANCE', 'BRITANNIA', 'AXISBANK', 'TECHM', 'COALINDIA', 'LT', 'DRREDDY', 'M_M', 'APOLLOHOSP', 'ADANIPORTS', 'BAJAJFINSV', 'GRASIM', 'TATACONSUM', 'ICICIBANK', 'HDFCBANK', 'EICHERMOT', 'BPCL', 'ADANIENT', 'UPL', 'POWERGRID', 'HDFCBANK', 'INFY', 'WIPRO', 'RELIANCE', 'INDUSINDBK', 'ASIANPAINT', 'HCLTECH', 'KOTAKBANK', 'BAJAJ_AUTO', 'SBIN'])

# index
for j in range(51):
    data_5_min = tv.get_hist(symbol=f'{n50_symbols[j]}',exchange='NSE',interval=Interval.in_5_minute,n_bars=5000)
    df=pd.DataFrame(data_5_min)
    df=df.reset_index()
    file_name = f'{n50_symbols[j]}.csv'
    try:
        existing_df = pd.read_csv(file_name)

        # print(existing_df['datetime'][5])
        last_dt=existing_df['datetime'][len(existing_df.index)-1] #the last date time of the exisisting df
        # print(type(datetime(last_dt)))
        for i in range(len(df)):
            if pd.to_datetime(df['datetime'][i]).timestamp()>pd.to_datetime(last_dt).timestamp():
                print(f"{pd.to_datetime(df['datetime'][i])} >  {pd.to_datetime(last_dt)}")
                df=df[i:]
                break

    except FileNotFoundError:
        existing_df = pd.DataFrame(columns=df.columns)  # Replace with your column names


    combined_df=pd.concat([existing_df,df],ignore_index=True)
    combined_df.to_csv(file_name, index=False)  
    print(j)
    time.sleep(10) # delay of 5 seconds to avoid timeout error   