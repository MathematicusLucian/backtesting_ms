# from datetime import date
import numpy as np
import pandas as pd
import pandas_ta as ta
# from ta import momentum
# import matplotlib.pyplot as plt
# import plotly.graph_objects as go
# from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()
# https://kernc.github.io/backtesting.py/doc/backtesting/#gsc.tab=0
from backtesting import Strategy
from backtesting.lib import crossover, SignalStrategy, TrailingStrategy
from backtesting.test import SMA
import pandas as pd

def SMA(values, n):
    return pd.Series(values).rolling(n).mean()

class SmaCross(Strategy):
    # n1 = None
    n1 = 10
    # n2 = None
    n2 = 20
    
    def init(self): #, n1=10, n2=20):
        Close1 = self.data.Close
        # print(self._params["n1"])
        # self.n1 = self._params["n1"]
        # self.n2 = self._params["n2"]
        self.sma1 = self.I(SMA, Close1, self.n1)
        self.sma2 = self.I(SMA, Close1, self.n2)
    
    def next(self):
        # print(f"\n\n{self._params}\n")
        # print(f"\n\n{self._params["n1"]}\n")
        # sma1 crosses above sma2 -> close short-trades, and buy the asset
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()
        # sma1 crosses below sma2 -> close long-trades, and sell the asset
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()

        # Consider day prior
        # if (self.sma1[-2] < self.sma2[-2] and self.sma1[-1] > self.sma2[-1]):
        #     self.position.close()
        #     self.buy()
        # elif (self.sma1[-2] > self.sma2[-2] and self.sma1[-1] < self.sma2[-1]):
        #     self.position.close()
        #     self.sell()

        # Multi-series
        # if crossover(series1=self.ma1, series2=self.ma2):
        #     self.buy()
        # elif crossover(series1=self.ma2, series2=self.ma1):
        #     self.sell()

class SmaCross__Trailing(SignalStrategy, TrailingStrategy):
    n1 = 10
    n2 = 25
    
    def init(self):
        super().init()
        sma1 = self.I(SMA, self.data.Close, self.n1)
        sma2 = self.I(SMA, self.data.Close, self.n2)
        # sma1 crosses sma2 upwards -> diff gives us [-1,0, *1*]
        signal = (pd.Series(sma1) > sma2).astype(int).diff().fillna(0)
        signal = signal.replace(-1, 0)  # upwards/long only
        entry_size = signal * .95 #  95% of available liquidity (at the time) on each order
        self.set_signal(entry_size=entry_size) #Set order entry sizes using the method provided by `SignalStrategy`. See the docs.
        self.set_trailing_sl(2) #Set trailing stop-loss to 2x ATR using the method provided by `TrailingStrategy`

class Sma4Cross(Strategy):
    n1 = 50
    n2 = 100
    n_enter = 20
    n_exit = 10
    
    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)
        self.sma_enter = self.I(SMA, self.data.Close, self.n_enter)
        self.sma_exit = self.I(SMA, self.data.Close, self.n_exit)
        
    def next(self):
        if not self.position:
            # upwards trend + price closes above "entry" MA -> go long
            if self.sma1 > self.sma2:
                if crossover(self.data.Close, self.sma_enter):
                    self.buy()
            else: # :. downwards trend + price closes below "entry" MA -> go short
                if crossover(self.sma_enter, self.data.Close):
                    self.sell()
        # holding a position + price closes back below (above) "exit" MA -> close the position
        else:
            if (self.position.is_long and crossover(self.sma_exit, self.data.Close) or
                    self.position.is_short and crossover(self.data.Close, self.sma_exit)):
                self.position.close()

def calculate_sma__days(df: pd.DataFrame, days):
    return ta.sma(df['Close'], int(days))

def calculate_sma(data, days_collection):
    for days in days_collection:
        data[f'SMA {days}'] = calculate_sma__days(data, days)
    # stock_pairs_dict[pair_name].to_csv(f'sma-{index}.csv', sep=',', index=False, encoding='utf-8')
    # data.to_csv(f'strategy-output-{pair_name}.csv', sep=',', index=False, encoding='utf-8')
    return data

def sma_strategy(data, signals):
    data[f'SMA {signals[0]}'], data[f'SMA {signals[1]}'] = sma_strategy_buy_sell(data)
    return data

def sma_strategy_buy_sell(df: pd.DataFrame):
    signalBuy = []
    signalSell = []
    position = False 

    for index, row in df.iterrows():
        if (row['SMA 30'] > row['SMA 10']) and (row['SMA 10'] > row['SMA 50']) and (row['SMA 30'] > row['SMA 50']) and (row['SMA 200'] > row['SMA 10']) and (row['SMA 200'] > row['SMA 30']) and (row['SMA 200'] > row['SMA 50']):
            if position == False:
                signalBuy.append(row['Adj Close'])
                signalSell.append(np.nan)
                position = True
            else:
                signalBuy.append(np.nan)
                signalSell.append(np.nan)
        elif (row['SMA 30'] < row['SMA 10']) and (row['SMA 10'] < row['SMA 50']) and (row['SMA 30'] < row['SMA 50']) and (row['SMA 200'] < row['SMA 10']) and (row['SMA 200'] < row['SMA 30']) and (row['SMA 200'] < row['SMA 50']):
            if position == True:
                signalBuy.append(np.nan)
                signalSell.append(row['Adj Close'])
                position = False
            else:
                signalBuy.append(np.nan)
                signalSell.append(np.nan)
        else:
            signalBuy.append(np.nan)
            signalSell.append(np.nan)
    return pd.Series([signalBuy, signalSell])

# Reuse composable base trading strategies that are part of backtesting.py software distribution
# bt = Backtest(GOOG, SmaCross, commission=.002)
# bt.run()
# bt.plot()

# bt = Backtest(GOOG, SmaCross, cash=10_000, commission=.002)
# stats = bt.run()
# stats = bt.optimize(n1=range(5, 30, 5),
#                     n2=range(10, 70, 5),
#                     maximize='Equity Final [$]',
#                     constraint=lambda param: param.n1 < param.n2)
# bt.plot(plot_volume=False, plot_pl=False)
