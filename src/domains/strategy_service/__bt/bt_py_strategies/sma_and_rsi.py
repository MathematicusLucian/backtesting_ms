from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import talib as ta

class SMAandRSI(Strategy):
    SMA_short = 10 
    SMA_long = 30 
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.SMA_short)
        self.sma2 = self.I(SMA, self.data.Close, self.SMA_long)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): 
        if self.rsi > self.upper_bound\
            or self.sma2 > self.sma1:
            self.position.close()
        elif self.lower_bound > self.rsi\
            and crossover(self.sma1, self.sma2):
            if not self.position:
                self.buy()

class SMAandRSI_WithShortPosition(Strategy):
    SMA_short = 10 
    SMA_long = 30 
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.SMA_short)
        self.sma2 = self.I(SMA, self.data.Close, self.SMA_long)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self):
        if self.rsi > self.upper_bound\
            or self.sma2 > self.sma1:
            if not self.position:
                self.sell()
            else:
                self.position.close()
        elif self.lower_bound > self.rsi\
            and crossover(self.sma1, self.sma2):
            if not self.position:
                self.buy()

class EntryRSIandExitSMA_WithShortPosition(Strategy):
    SMA_short = 10 
    SMA_long = 30
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.SMA_short)
        self.sma2 = self.I(SMA, self.data.Close, self.SMA_long)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self):
        price = self.data.Close[-1]
        if crossover(self.sma2, self.sma1) or crossover(self.sma1, self.sma2):
            self.position.close()
        elif self.upper_bound < self.rsi:
            if not self.position:
                self.sell()
        elif self.lower_bound > self.rsi:
            if not self.position:
                self.buy(tp = 1.15 * price, sl = 0.95*price)