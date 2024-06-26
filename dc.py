from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import talib as ta

def day_num(day):
    switcher = {
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5
    }
    return switcher.get(day)

tv = TvDatafeed()

nifty_symbols = [
    "ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV",
    "BAJFINANCE", "BPCL", "BRITANNIA", "CIPLA", "COALINDIA",
    "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH",
    "HDFCBANK", "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDUNILVR",
    "ICICIBANK", "ICICIGI", "IOC", "INDUSINDBK", "INFY",
    "ITC", "JSWSTEEL", "KOTAKBANK", "LTTS", "LT",
    "M&M", "MARICO", "MARUTI", "NESTLEIND"
]


columns = ['datetime', 'symbol', 'close', 'volume', 'day', 'time']

df = pd.DataFrame(columns=columns)

for symbol in nifty_symbols:
    symbol_data = tv.get_hist(symbol=symbol, exchange="NSE", interval=Interval.in_15_minute, n_bars=500)
    if symbol_data is not None:
        
        symbol_data.reset_index(inplace=True)
        symbol_data['datetime'] = pd.to_datetime(symbol_data['datetime'])
        symbol_data['day'] = symbol_data['datetime'].dt.day_name().apply(day_num)
        start_of_day = symbol_data['datetime'].dt.normalize()
        symbol_data['time'] = (symbol_data['datetime'] - start_of_day).dt.total_seconds()
        
        
        df = pd.concat([df, symbol_data], ignore_index=True)


df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)


df['RSI'] = ta.RSI(df['close'], timeperiod=14)
macd, macdsignal, macdhist = ta.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
df['MACD'] = macd


df['Change'] = (df['close'].shift(-1) > df['close']).astype(int)


df.drop(['datetime','symbol'], axis=1, inplace=True)

df.dropna(inplace=True)
df.to_csv('Total_data.csv', index=False)


print(df)
