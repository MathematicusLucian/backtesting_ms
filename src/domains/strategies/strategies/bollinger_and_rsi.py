from backtesting import Strategy
from backtesting.lib import crossover
import talib as ta
import pandas as pd
import numpy as np
from src.strategies.bollinger import BBANDS_2

def CalcATR(phigh, plow, pclose, period):
    high = pd.Series(phigh)
    low = pd.Series(plow)
    close = pd.Series(pclose)
    return ta.ATR(\
        np.array(high).astype("double"),\
        np.array(low).astype("double"),\
        np.array(close).astype("double"),\
        timeperiod=period)

class BBandRSI(Strategy):
    n = 25 
    nu = 2 
    nd = 2 
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.upper, self.lower = self.I(BBANDS_2, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): 
        if self.data.Close > self.upper\
            or crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif self.data.Close < self.lower\
            and crossover(self.lower_bound, self.rsi):
            if not self.position:
                self.buy() 

class BBandRSI_WithStopLoss(Strategy):
    n = 25 
    nu = 2 
    nd = 2 
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14
    stop_loss_perc = -7.5

    def init(self):
        self.upper, self.lower = self.I(BBANDS_2, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): 
        price = self.data.Close
        if self.position:
            if self.position.pl_pct < self.stop_loss_perc:
                print(self.position.pl_pct)
                self.position.close()
        if self.data.High > self.upper\
            or crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif self.data.Low < self.lower\
            or crossover(self.lower_bound, self.rsi):
            if not self.position:
                self.buy() 

class BBandRSI_WithShortPosition(Strategy):
    n = 25 
    nu = 2 
    nd = 2 
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.upper, self.lower = self.I(BBANDS_2, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): 
        if self.data.Close > self.upper\
            or crossover(self.rsi, self.upper_bound):
            if not self.position:
                self.sell()
            else:
                self.position.close()
        elif self.data.Close < self.lower\
            or crossover(self.lower_bound, self.rsi):
            if not self.position:
                self.buy() 

class EntryRSI50andExitBB(Strategy):
    n = 25 
    nu = 2
    nd = 2 
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.upper, self.lower = self.I(BBANDS_2, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): 
        rsi_previous = self.rsi[-1]
        rsi_2previous = self.rsi[-2]

        if self.data.Close > self.upper or self.data.Low > self.upper:
            if self.position:
                self.position.close()
        elif rsi_2previous < 50 and rsi_previous > 50:
            if not self.position:
                self.buy() 
        elif rsi_previous < 40:
            if self.position and self.trades[-1].size > 0:
                self.position.close()
        elif rsi_previous < 60:
            if self.position and self.trades[-1].size < 0:
                self.position.close()

class EntryRSI50andExitBB_WithShortPosition(Strategy):
    n = 25 
    nu = 2 
    nd = 2 
    upper_bound = 50
    lower_bound = 50
    rsi_window = 14

    def init(self):
        self.upper, self.lower = self.I(BBANDS_2, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): 
        rsi_previous = self.rsi[-1]
        rsi_2previous = self.rsi[-2]

        if self.data.Close > self.upper and self.position:
            if self.position and self.trades[-1].size > 0:
                self.position.close()
        elif self.data.Close < self.lower and self.position:
            if self.position and self.trades[-1].size < 0:
                self.position.close()
        elif rsi_2previous < 50 and rsi_previous > 50:
            if not self.position:
                self.buy()
        elif rsi_2previous > 50 and rsi_previous < 50:
            if not self.position:
                self.sell()
        if rsi_previous < 40:
            if self.position and self.trades[-1].size > 0:
                self.position.close()
        if rsi_previous < 60:        
            if self.position and self.trades[-1].size < 0:
                self.position.close()

class EntryRSI50andExitBBWithATRStopLoss(Strategy):
    n = 25
    nu = 2
    nd = 2 
    upper_bound = 50
    lower_bound = 50
    rsi_window = 14
    atr_period = 20

    def init(self):
        self.upper, self.lower = self.I(BBANDS_2, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)
        self.atr = self.I(CalcATR, self.data.High,  self.data.Low, self.data.Close, self.atr_period)

    def next(self): 
        rsi_previous = self.rsi[-1]
        rsi_2previous = self.rsi[-2]

        if self.data.Close > self.upper and self.position and self.trades[-1].size > 0:
            self.position.close()
        elif self.position and self.data.Close[-1] < self.trades[-1].entry_price - self.atr[-1] * 2:
            self.position.close()
        elif self.data.Close > self.lower and self.position and self.trades[-1].size < 0:
            self.position.close()
        elif self.position and self.data.Close[-1] > self.trades[-1].entry_price + self.atr[-1] * 2:
            self.position.close()
        elif rsi_2previous < 50 and rsi_previous > 50:
            if not self.position:
                self.buy()
        elif rsi_2previous > 50 and rsi_previous < 50:
            if not self.position:
                self.sell()