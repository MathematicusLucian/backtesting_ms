from datetime import date
import numpy as np
import pandas as pd
import pandas_ta as ta
from ta import momentum
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()
from backtesting import Strategy
from backtesting.lib import crossover, resample_apply
from backtesting.test import GOOG

class RsiOscillator__Simple(Strategy):
    ww_rsi = 14
    oversold_level = 30
    overbought_level = 70

    def init(self):
        Close1 = self.data.Close
        self.rsi_14 = self.I(rsi, Close1, self.ww_rsi)

    def next(self):
        if self.rsi_14 < self.oversold_level:
            self.buy()
        elif self.rsi_14 > self.overbought_level:
            self.sell()

class RsiOscillator__Simple_Close(Strategy):
    ww_rsi = 14
    oversold_level = 20
    overbought_level = 80

    def init(self):
        Close1 = self.data.Close
        self.rsi_14 = self.I(rsi, Close1, self.ww_rsi)

    def next(self):
        if not self.position:
            if self.rsi_14 < self.oversold_level:
                self.buy()
            elif self.rsi_14 > self.overbought_level:
                self.sell()
        if self.position:
            if self.rsi_14 < self.oversold_level:
                self.position.close()
            elif self.rsi_14 > self.overbought_level:
                self.position.close()

class RsiOscillator(Strategy):
    upper_bound=60
    lower_bound=40
    rsi_window=12
    atr_window=14
    atr_stoploss=4
    atr_takeprofit=8

    def init(self):
        self.rsi = self.I(ta.rsi, self.data.Close, self.rsi_window)
        self.atr = self.I(ta.ATR, self.data.High , self.data.Low, self.data.Close, self.atr_window)

    def next(self): 
        if self.position:
            price = self.trades[-1].entry_price
            if self.data.Low[-1] > price + (self.atr[-1] * self.atr_takeprofit) or\
                self.data.Low[-1] < price - (self.atr[-1] * self.atr_stoploss):
                if self.data.Low[-1] > price + (self.atr[-1] * self.atr_takeprofit):
                    print("take profit  " + str(self.data.index[-1]) + "  " +
                    str(price) + "  " + str(price + (self.atr[-1] * self.atr_takeprofit)))
                if self.data.Low[-1] < price - (self.atr[-1] * self.atr_stoploss):
                    print("stop loss  " + str(self.data.index[-1]) + "  " +
                    str(price) + "  " + str(price - (self.atr[-1] * self.atr_stoploss)))
                self.position.close()
            elif crossover(self.upper_bound, self.rsi):
                print("RSI close " + str(self.data.index[-1]))
                self.position.close()
        elif crossover(self.lower_bound, self.rsi):
            if not self.position:
                self.buy()

class RsiOscillator__Single(Strategy):
    def init(self): #, *args, **kwargs): # upper_bound, lower_bound, rsi_window, tp=None, sl=None, size=None,
        # super(RsiOscillator__Single, self).__init__(self, upper_bound, lower_bound, rsi_window, tp=None, sl=None)
        # super().__init__(*args, **kwargs)
        # super().init(self, *args, **kwargs)
    #     self.upper_bound = upper_bound
    #     self.lower_bound = lower_bound
    #     self.rsi_window = rsi_window
    #     self.sl = sl
    #     self.tp = tp
    #     self.size = size
    #     self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_window)
        print(self.params)

    def next(self):
        price = self.data.Close[-1]
    #     if crossover(self.rsi, self.upper_bound):
    #         self.position.close()
    #     elif crossover(self.lower_bound, self.rsi):
    #         if self.tp != None and self.sl !=None:
    #             self.buy(tp=self.tp*price, sl=self.sl*price)
    #         elif self.size != None:
    #             self.buy(size=0.1)
    #         else:
    #             self.buy()

class RsiOscillator__DailyWeekly(Strategy):
    def init(self, upper_bound, lower_bound, rsi_window):
        super(RsiOscillator__DailyWeekly, self).__init__(upper_bound, lower_bound, rsi_window, tp=None, sl=None)
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.rsi_window = rsi_window
        self.daily_rsi = self.I(ta.rsiI, pd.Series(self.data.Close), self.rsi_window)
        self.weekly_rsi = resample_apply(
            'W-FRI', ta.rsi, pd.Series(self.data.Close), self.rsi_window
        )

    def next(self):
        if (crossover(self.daily_rsi, self.upper_bound) and
                self.weekly_rsi[-1] > self.upper_bound):
            self.position.close()
        elif (crossover(self.lower_bound, self.daily_rsi) and
                self.lower_bound > self.weekly_rsi[-1]):
            self.buy()

class RsiOscillator__LS_Close(Strategy):
    s_rsi = 6
    l_rsi = 24
    ww_rsi = 14
    oversold_level = 20
    overbought_level = 80

    def init(self):
        Close1 = self.data.Close
        self.rsi_14 = self.I(rsi, Close1, self.ww_rsi)

        self.st_rsi = self.I(rsi, Close1, self.s_rsi)
        self.lt_rsi = self.I(rsi, Close1, self.l_rsi)

    def next(self):
        if not self.position:
            if self.st_rsi < self.oversold_level and self.lt_rsi < self.oversold_level:
                self.buy()
            elif self.st_rsi > self.overbought_level and self.lt_rsi > self.overbought_level:
                self.sell()
        if self.position:
            if self.st_rsi < self.oversold_level or self.lt_rsi < self.oversold_level:
                self.position.close()
            elif self.st_rsi > self.overbought_level or self.lt_rsi > self.overbought_level:
                self.position.close()

def relative_strength_index(df: pd.DataFrame, days):
    return ta.rsi(df['Close'], int(days))

def rsi(array, n):
    gain = pd.Series(array).diff()
    loss = gain.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    rs = gain.rolling(n).mean() / loss.abs().rolling(n).mean()
    return 100 - 100 / (1 + rs)

