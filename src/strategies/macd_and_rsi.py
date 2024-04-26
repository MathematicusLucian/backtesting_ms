import pandas_ta as ta
import yfinance as yfin
yfin.pdr_override()
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
from src.strategies.macd import calculate_macd_2

class MACDandRSI(Strategy):
    MACDshort = 12 
    MACDlong = 26 
    MACDsignal = 9 
    MACDThreshold = 0
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.macd, self.macdsignal = self.I(calculate_macd_2, self.data.Close, self.MACDshort, self.MACDlong, self.MACDsignal)
        self.rsi = self.I(ta.rsi, self.data.Close, self.rsi_window)

    def next(self): 
        if self.rsi[-1] > self.upper_bound or self.macd > self.MACDThreshold and self.macdsignal > self.MACDThreshold and crossover(self.macdsignal, self.macd):
            self.position.close()
        elif self.rsi[-1] < self.lower_bound and self.macd < self.MACDThreshold and self.macdsignal < self.MACDThreshold and crossover(self.macd, self.macdsignal):
            if not self.position:
                self.buy() 

class MACDandRSI_WithShortPosition(Strategy):
    MACDshort = 12 
    MACDlong = 26 
    MACDsignal = 9 
    MACDThreshold = 0
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.macd, self.macdsignal = self.I(calculate_macd_2, self.data.Close, self.MACDshort, self.MACDlong, self.MACDsignal)
        self.rsi = self.I(ta.rsi, self.data.Close, self.rsi_window)

    def next(self): 
        if self.rsi[-1] > self.upper_bound or self.macd > self.MACDThreshold and self.macdsignal > self.MACDThreshold and crossover(self.macdsignal, self.macd):
            if not self.position:
                self.sell()
            else:
                self.position.close()
        elif self.rsi[-1] < self.lower_bound and self.macd < self.MACDThreshold and self.macdsignal < self.MACDThreshold and crossover(self.macd, self.macdsignal):
            if not self.position:
                self.buy()