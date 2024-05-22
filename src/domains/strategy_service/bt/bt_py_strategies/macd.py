from datetime import datetime, date
import numpy as np
import pandas as pd
import pandas_ta as ta
import pandas_datareader as web
from ta import momentum
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import yfinance as yfin
yfin.pdr_override()
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

class MACDStrategy(Strategy):
    params = (
        ('fast', 12), #12 day EMA
        ('slow', 26), #23 day EMA
        ('signal', 9), #9 day EMA
    )
    # macd = 0
    # macd_signal = 0

    def init(self):
        close = pd.Series(self.data.Close)
        fast = int(self.params[0][1])
        slow = int(self.params[1][1])
        signal = int(self.params[2][1])
        macd, signal = self.macd(close, fast, slow, signal)
        macd_diff = macd - signal
        self.macd_diff = self.I(macd_diff)
        # print(f"\n\n{macd - signal}")

    def next(self):
        pass
        # if self.macd_diff.crossed_above(0):
        # if crossover(self.macd, self.macd_signal):
            # self.buy()
        # elif self.macd_diff.crossed_below(0):
        # if crossover(self.macd_signal, self.macd):
            # self.sell()

    def macd(self, close, fast, slow, signal):
        exp1 = close.ewm(span=fast, adjust=False).mean()
        exp2 = close.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=signal, adjust=False).mean()
        return macd, signal
    
    # def macd_other_method(self):
    #     price = self.data.Close
    #     self.macd = self.I(lambda x: talib.MACD(x)[0], price)
    #     self.macd_signal = self.I(lambda x: talib.MACD(x)[1], price)

class MACDCross(Strategy):
    MACD_short = 12 
    MACD_long = 26
    MACD_signal = 9 
    MACD_threshold_plus = 0
    MACD_threshold_minus = -150

    def init(self):
        self.macd, self.MACD_signal, self.macdhist = self.I(calculate_macd_2, self.data.Close, self.MACD_short, self.MACD_long, self.MACD_signal)

    def next(self): 
        if self.macd < self.MACD_threshold_minus and self.MACD_signal < self.MACD_threshold_minus and crossover(self.macd, self.MACD_signal):
            if not self.position:
                self.buy() 
        elif self.position and self.macdhist[-1] < self.macdhist[-2] and self.macdhist[-2] < self.macdhist[-3]:
            self.position.close()
        elif self.position and crossover(self.MACD_signal, self.macd):
            self.position.close()

class MACDCross_WithShortPosition(Strategy):
    MACD_short = 12 
    MACD_long = 26 
    MACD_signal = 9 
    MACD_threshold_plus = 460
    MACD_threshold_minus = -140

    def init(self):
        self.macd, self.MACD_signal, self.macdhist = self.I(calculate_macd_2, self.data.Close, self.MACD_short, self.MACD_long, self.MACD_signal)

    def next(self): 
        if self.macd < self.MACD_threshold_minus and self.MACD_signal < self.MACD_threshold_minus and crossover(self.macd, self.MACD_signal):
            if not self.position:
                self.buy() 
        elif self.macd > self.MACD_threshold_plus and self.MACD_signal > self.MACD_threshold_plus and crossover(self.MACD_signal, self.macd):
            if not self.position:
                self.sell() 
        elif self.position.is_long and self.macdhist[-1] < self.macdhist[-2] and self.macdhist[-2] < self.macdhist[-3]:
            self.position.close()
        elif self.position.is_short and self.macdhist[-1] > self.macdhist[-2] and self.macdhist[-2] > self.macdhist[-3]:
            self.position.close()
        elif self.position.is_long and crossover(self.MACD_signal, self.macd):
            self.position.close()
        elif self.position.is_short and crossover(self.macd, self.MACD_signal):
            self.position.close()

def calculate_macd(df) -> pd.DataFrame:
    df_macd = ta.macd(df['Close'])
    return pd.concat([df, df_macd], axis=1).reindex(df.index)

def calculate_macd_2(close, macd_short, macd_long, macd_signal):
    macd, macd_signal, macd_hist = ta.macd(close, fastperiod=macd_short, slowperiod=macd_long, signalperiod=macd_signal)
    return macd, macd_signal, macd_hist

def calculate_macd_trend(df) -> pd.DataFrame:
    macd_trend = ta.trend.MACD(df['Close'])
    df['MACD'] = macd_trend.macd()
    df['MACD_Signal'] = macd_trend.macd_signal()
    df['MACD_Diff'] = macd_trend.macd_diff()
    df.tail()
    return df

def add_macd_signal_indicators__adj_close(df):
    macd = ta.macd(df['Adj Close'], fast=12, slow=26, signal=9)
    df['MACD'] = macd['MACD_12_26_9']
    df['MACD_signal'] = macd['MACDs_12_26_9']
    df['MACD_hist'] = macd['MACDh_12_26_9']
    df['10_cross_30'] = np.where(df['SMA_10'] > df['SMA_30'], 1, 0)
    df['MACD_Signal_MACD'] = np.where(df['MACD_signal'] < df['MACD'], 1, 0)
    df['MACD_lim'] = np.where(df['MACD']>0, 1, 0)
    df['abv_50'] = np.where((df['SMA_30']>df['SMA_50'])&(df['SMA_10']>df['SMA_50']), 1, 0)
    df['abv_200'] = np.where((df['SMA_30']>df['SMA_200'])&(df['SMA_10']>df['SMA_200'])&(df['SMA_50']>df['SMA_200']), 1, 0)
    return df

def macd_color(df):
    macd_color = []
    for (index, row), ii in zip(df.iterrows(), range(len(df.index))):
        if row['MACDh_12_26_9'] > df.iloc[ii-1]['MACDh_12_26_9']:
            macd_color.append(True)
        else:
            macd_color.append(False)
    return macd_color

def macd_strategy(df, risk):
    MACD_Buy=[]
    MACD_Sell=[]
    position=False

    for (index, row), ii in zip(df.iterrows(), range(len(df.index))):
        if row['MACD_12_26_9'] > row['MACDs_12_26_9']:
            MACD_Sell.append(np.nan)
            if position ==False:
                MACD_Buy.append(row['Adj Close'])
                position=True
            else:
                MACD_Buy.append(np.nan)
        elif row['MACD_12_26_9'] < row['MACDs_12_26_9']:
            MACD_Buy.append(np.nan)
            if position == True:
                MACD_Sell.append(row['Adj Close'])
                position=False
            else:
                MACD_Sell.append(np.nan)
        elif position == True and row['Adj Close'] < MACD_Buy[-1] * (1 - risk):
            MACD_Sell.append(row['Adj Close'])
            MACD_Buy.append(np.nan)
            position = False
        elif position == True and row['Adj Close'] < df.iloc[ii-1]['Adj Close'] * (1 - risk):
            MACD_Sell.append(row['Adj Close'])
            MACD_Buy.append(np.nan)
            position = False
        else:
            MACD_Buy.append(np.nan)
            MACD_Sell.append(np.nan)

    df['MACD_Buy_Signal_price'] = MACD_Buy
    df['MACD_Sell_Signal_price'] = MACD_Sell
    df['positive'] = macd_color(df)
    return df

# bt = Backtest(GOOG, MACDStrategy, cash=10000, commission=.002, exclusive_orders=True)
# results = bt.run()
# print(results)
# bt.plot()