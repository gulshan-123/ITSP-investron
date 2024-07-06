import numpy as np
import pandas as pd
import talib as ta

class MockBroker():
    def __init__(self,Balance):
        self.holdings = {}
        self.Balance = Balance

    def __str__(self):
        return str(self.holdings) + "\n Balance: "+ str(self.Balance)

    def buy(self, stock, price, qty):
        if (self.Balance >= price*int(qty)):
            org_qty = int(self.holdings.get(stock)) if self.holdings.get(stock) else 0
            self.holdings.update({stock: int(org_qty)+int(qty)})
            self.Balance -= price*int(qty)
            print(self.holdings)
            print("Balance: " + str(self.Balance))
        else:
            print("Not enough Balance")
    

    def sell(self, stock,price, qty):
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

