import numpy as np
import pandas as pd
import talib as ta
from tvDatafeed import TvDatafeed, Interval



class MockMarket():
    def __init__(self,Balance):
        self.holdings = {}
        self.tv = TvDatafeed()
        self.Balance = Balance

    def __str__(self):
        return str(self.holdings) + "\n Balance: "+ str(self.Balance)

    def buy(self, stock, qty):
        stock_data = pd.DataFrame(self.tv.get_hist(symbol=stock, exchange='NSE', interval=Interval.in_1_minute, n_bars=1))
        price = int(stock_data['close'].iloc[0])
        if (self.Balance >= price*int(qty)):
            org_qty = int(self.holdings.get(stock)) if self.holdings.get(stock) else 0
            self.holdings.update({stock: int(org_qty)+int(qty)})
            self.Balance -= price*int(qty)
            print(self.holdings)
            print("Balance: " + str(self.Balance))
        else:
            print("Not enough Balance")
    

    def sell(self, stock,qty):
        stock_data = pd.DataFrame(self.tv.get_hist(symbol=stock, exchange='NSE', interval=Interval.in_1_minute, n_bars=1))
        price = int(stock_data['close'].iloc[0])
        org_qty = int(self.holdings.get(stock, 0))
        if (self.Balance >= price*int(qty)):
            if (org_qty>=int(qty)):
                self.holdings.update({stock: int(org_qty)-int(qty)})
                self.Balance -= price*int(qty)
                print(self.holdings)
                print("Balance: " + str(self.Balance))
            else:
                print("Cant sell more than bought")
        else:
            print("Not Enough Balance")

    def get_holdings(self):
        return self.holdings

