from MockMarket import MockMarket

BALANCE = 100000

s = MockMarket(BALANCE)
s.buy('RELIANCE', 2)
s.buy('ADANIENT', 3)

s.buy('RELIANCE', 4)
s.sell('ADANIENT', 2)

s.sell('RELIANCE',4)

s.sell('RELIANCE',1)
print(s)