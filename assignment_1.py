from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import talib as ta

tv = TvDatafeed('vistasflamingo','Gulshan@2575')


reliance_data = tv.get_hist(symbol="RELIANCE", exchange='NSE', interval=Interval.in_5_minute, n_bars=5000)

reliance_data['RSI'] = ta.RSI(reliance_data['close'], timeperiod=14)
reliance_data['EMA_26'] = ta.EMA(reliance_data['close'], timeperiod=26)
reliance_data['EMA_200'] = ta.EMA(reliance_data['close'], timeperiod=200)
macd, macdsignal, macdhist = ta.MACD(reliance_data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
reliance_data['MACD'] = macd


reliance_data.dropna(inplace=True)

reliance_data = reliance_data.reset_index()
reliance_data['Position'] = 'Hold'
reliance_data.loc[((reliance_data['EMA_200'] > reliance_data['close']) & (reliance_data['MACD'] > 0)), 'Position'] = 'Buy'
reliance_data.loc[((reliance_data['EMA_200'] < reliance_data['close']) & (reliance_data['MACD'] < 0)), 'Position'] = 'Sell'

reliance_data.to_csv('result.csv')
print(reliance_data)