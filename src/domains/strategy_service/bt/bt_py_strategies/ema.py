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

def EMA_Backtesting(values, n):
    close = pd.Series(values)
    return ta.EMA(close, timeperiod=n)

class EMA_Cross(Strategy):
    EMA_short = 10
    EMA_long = 20

    def init(self):
        Close1 = self.data.Close
        self.ma1 = self.I(func=self.ema, values=Close1, n=self.EMA_short)
        self.ma2 = self.I(func=self.ema, values=Close1, n=self.EMA_long)

    def next(self):
        if crossover(series1=self.ma1, series2=self.ma2):
            self.buy()
        elif crossover(series1=self.ma2, series2=self.ma1):
            self.sell()

    def ema(self, values, n):
        return pd.Series(values).ewm(span=n).mean()

class Ema_Cross2(Strategy):
    EMA_short = 5
    EMA_long = 10

    def init(self):
        self.ema1 = self.I(EMA_Backtesting, self.data.Close, self.EMA_short)
        self.ema2 = self.I(EMA_Backtesting, self.data.Close, self.EMA_long)

    def next(self):
        if crossover(self.ema1, self.ema2):
            if not self.position:
                self.buy() 
        elif crossover(self.ema2, self.ema1):
            self.position.close()

class Ema_Cross__WithShortPosition(Strategy):
    EMAshort = 5
    EMAlong = 10

    def init(self):
        self.ema1 = self.I(EMA_Backtesting, self.data.Close, self.EMAshort)
        self.ema2 = self.I(EMA_Backtesting, self.data.Close, self.EMAlong)

    def next(self):
        if crossover(self.ema1, self.ema2):
            if not self.position:
                self.buy() 
        elif crossover(self.ema2, self.ema1):
            if not self.position:
                self.sell()
            else:
                self.position.close()

def calculate_ema(df) -> pd.DataFrame:
    df["ema12"] = ta.ema(df["close"], length=12, fillna=df.close)
    df["ema26"] = ta.ema(df["close"], length=26, fillna=df.close)
    df["ema12gtema26"] = df.ema12 > df.ema26
    df["ema12gtema26co"] = df.ema12gtema26.ne(df.ema12gtema26.shift())
    df.loc[df["ema12gtema26"] == 0, "ema12gtema26co"] = 0
    df["ema12ltema26"] = df.ema12 < df.ema26
    df["ema12ltema26co"] = df.ema12ltema26.ne(df.ema12ltema26.shift())
    df.loc[df["ema12ltema26"] == 0, "ema12ltema26co"] = 0
    df["ema12gtema26"] = df["ema12gtema26"].astype(int)
    df["ema12gtema26co"] = df["ema12gtema26co"].astype(int)
    df["ema12ltema26"] = df["ema12ltema26"].astype(int)
    df["ema12ltema26co"] = df["ema12ltema26co"].astype(int)
    return df

def signals(df):
    buysignals = df[df["ema12gtema26co"] == 1]
    sellsignals = df[df["ema12ltema26co"] == 1]
    return buysignals, sellsignals