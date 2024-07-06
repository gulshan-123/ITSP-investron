from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import numpy as np
import talib as ta
import os


tv = TvDatafeed()

nifty_symbols = [
    "ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJFINSV",
    "BAJFINANCE", "BPCL", "BRITANNIA", "CIPLA", "COALINDIA",
    "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH",
    "HDFCBANK", "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDUNILVR",
    "ICICIBANK", "ICICIGI", "IOC", "INDUSINDBK", "INFY",
    "ITC", "JSWSTEEL", "KOTAKBANK", "LTTS", "LT",
    "MARICO", "MARUTI", "NESTLEIND"
]
#bajaj-auto and mAnd M dont work

# nifty_symbols = ["ADANIPORTS"]
percent_10 = 0.5  # will experiment here
output_dir = 'data'


if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def calculate_fibonacci_levels(high, low):
    levels = [0.236, 0.382, 0.5, 0.618, 1.0]  # Fibonacci levels
    diff = high - low
    fib_levels = [low + level * diff for level in levels]
    return fib_levels

while(nifty_symbols):
    for symbol in nifty_symbols:
        try :

        
            df = tv.get_hist(symbol=symbol, exchange="NSE", interval=Interval.in_daily, n_bars=10000)
            
            if df is not None and not df.empty:

                df.reset_index(inplace=True)
                
                # Calculate MACD using TA-Lib
                macd, macdsignal, macdhist = ta.MACD(df['close'], fastperiod=6, slowperiod=15, signalperiod=2)
                
                # Add MACD and signal to the DataFrame
                df['MACD'] = macd
                
                df['Percent'] = df['close'].pct_change()
                df['Percent'] = df['Percent'].shift(-1)
                # Define buy, sell, hold positions based on percentage change
                # df['Position'] = np.where(df['Percent'] > percent_10, 1, np.where(df['Percent'] < percent_10 , -1,0))
                df['MACDandSIG'] = macd-macdsignal
                # previous_value = None
                # for i in range(len(df)):
                #     current_value = df.at[i, 'MACDandSIG']
                #     if current_value == previous_value:
                #         df.at[i, 'MACDandSIG'] = 0
                #     else:
                #         previous_value = current_value
                # optional depends .right now it helps the process. can change it to a strategy
                # make training easier


                df.dropna(inplace=True)
            
                
                
                df['RSI'] = ta.RSI(df['close'], timeperiod=14)
                # df['RSI'] = np.where((df['RSI'] > 70) | (df['RSI'] < 30), (df['RSI']-50), 0)
                df['RSI'] = df['RSI']-50
                
                # previous_value = None
                # for i in range(len(df)):
                #     current_value = df.at[i, 'RSI']
                #     if current_value == previous_value:
                #         df.at[i, 'RSI'] = 0
                #     else:
                #         previous_value = current_value
                #           can change this for hold
                # remember rsi has to wait for a few days

                df['20ma'] = df['close'].rolling(window=20).mean()
                df['stddev'] = df['close'].rolling(window=20).std()

                # Calculate upper and lower Bollinger Bands
                df['upper_band'] = df['20ma'] + 2 * df['stddev']
                df['lower_band'] = df['20ma'] - 2 * df['stddev']

                # Generate buy/sell signals
                df['Bollinger'] = 0  # Default to hold

                # Buy signal: price crosses below lower band
                df.loc[df['close'] < df['lower_band'], 'Bollinger'] = df['lower_band']-df['close']

                # Sell signal: price crosses above upper band
                df.loc[df['close'] > df['upper_band'], 'Bollinger'] = df['upper_band']-df['close']



                high = df['close'].max()
                low = df['close'].min()
                fib_levels = calculate_fibonacci_levels(high, low)

                # Generate Fibonacci signals
                df['Fibonacci'] = 0  # Default to hold

                # Buy signal: price touches Fibonacci support levels
                for level in fib_levels:
                    df.loc[df['close'] <= level, 'Fibonacci'] = 1

                # Sell signal: price touches Fibonacci resistance levels
                for level in fib_levels:
                    df.loc[df['close'] >= level, 'Fibonacci'] = -1

                df = df.iloc[14:]

                # Reset the index to maintain the continuity of the DataFrame's index
                df.reset_index(drop=True, inplace=True)

                result_df = df[['close','MACD','MACDandSIG','RSI','Bollinger','Fibonacci', 'Percent']]

                csv_filename = f"{output_dir}/{symbol}.csv"
                result_df.to_csv(csv_filename, index=False)
                
                print(f"Data for {symbol} saved to {csv_filename}.")
                nifty_symbols.remove(symbol)
                print(nifty_symbols)
                
        except:
                print(f"No data fetched for {symbol}.")
                


