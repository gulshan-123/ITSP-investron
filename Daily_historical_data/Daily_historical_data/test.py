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


data_5_min = tv.get_hist(symbol='BAJAJ_AUTO',exchange='NSE',interval=Interval.in_5_minute,n_bars=5000)
df=pd.DataFrame(data_5_min)
print(df)