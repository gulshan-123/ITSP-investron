from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import numpy as np
import talib as tb
import time
import os
import pywhatkit
import matplotlib.pyplot as plt

tv = TvDatafeed()

n50_symbols=np.array(['NIFTY', 'HINDALCO', 'MARUTI', 'NESTLEIND', 'ONGC', 'TATAMOTORS', 'ITC', 'SUNPHARMA', 'BHARTIARTL', 'CIPLA', 'DIVISLAB', 'JSWSTEEL', 'HINDUNILVR', 'TITAN', 'NTPC', 'TATASTEEL', 'HEROMOTOCO', 'HDFCLIFE', 'ULTRACEMCO', 'SBILIFE', 'TCS', 'BAJFINANCE', 'BRITANNIA', 'AXISBANK', 'TECHM', 'COALINDIA', 'LT', 'DRREDDY', 'M_M', 'APOLLOHOSP', 'ADANIPORTS', 'BAJAJFINSV', 'GRASIM', 'TATACONSUM', 'ICICIBANK', 'HDFCBANK', 'EICHERMOT', 'BPCL', 'ADANIENT', 'UPL', 'POWERGRID', 'HDFCBANK', 'INFY', 'WIPRO', 'RELIANCE', 'INDUSINDBK', 'ASIANPAINT', 'HCLTECH', 'KOTAKBANK', 'BAJAJ_AUTO', 'SBIN'])

# index
for j in range(51):    
    file_name = f'{n50_symbols[j]}.csv'
    df = pd.read_csv(file_name)

    # Drop the last 5000 rows
    df = pd.DataFrame()

    # Save the modified DataFrame back to a CSV file
    output_csv_path = f'{n50_symbols[j]}.csv'
    df.to_csv(output_csv_path, index=False)
