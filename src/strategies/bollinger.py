from datetime import date
import numpy as np
import pandas as pd
from ta import momentum
import pandas_ta as pta
import talib as ta
from finta import TA
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()

def BBANDS(data, n_lookback, n_std):
    """Bollinger bands indicator"""
    hlc3 = (data.High + data.Low + data.Close) / 3
    mean, std = hlc3.rolling(n_lookback).mean(), hlc3.rolling(n_lookback).std()
    upper = mean + n_std*std
    lower = mean - n_std*std
    return upper, lower

def BBANDS_2(close, n, nu, nd):
    # df["upper"], df["middle"], df["lower"] = ta.BBANDS(close, timeperiod=span02, nbdevdn=2, nbdevup = 2, matype = 0)
    upper, middle, lower = ta.BBANDS(close, timeperiod=n, nbdevup=nu, nbdevdn=nd, matype=0)
    return upper, lower

def bbands(data, SMA):
    close = data.Close.values
    sma10 = SMA(data.Close, 10)
    sma20 = SMA(data.Close, 20)
    sma50 = SMA(data.Close, 50)
    sma100 = SMA(data.Close, 100)
    upper, lower = BBANDS(data, 20, 2)

    # Design matrix / independent features:

    # Price-derived features
    data['X_SMA10'] = (close - sma10) / close
    data['X_SMA20'] = (close - sma20) / close
    data['X_SMA50'] = (close - sma50) / close
    data['X_SMA100'] = (close - sma100) / close

    data['X_DELTA_SMA10'] = (sma10 - sma20) / close
    data['X_DELTA_SMA20'] = (sma20 - sma50) / close
    data['X_DELTA_SMA50'] = (sma50 - sma100) / close

    # Indicator features
    data['X_MOM'] = data.Close.pct_change(periods=2)
    data['X_BB_upper'] = (upper - close) / close
    data['X_BB_lower'] = (lower - close) / close
    data['X_BB_width'] = (upper - lower) / close
    data['X_Sentiment'] = ~data.index.to_series().between('2017-09-27', '2017-12-14')

    # Some datetime features for good measure
    data['X_day'] = data.index.dayofweek
    data['X_hour'] = data.index.hour

    data = data.dropna().astype(float)
    return data

def calculate_bollinger(df):
    bb = pta.bbands(df['Adj Close'], length=20,std=2)
    df = pd.concat([df, bb], axis=1).reindex(df.index)
    return df

# def bands(df):
#     upper, middle, lower = talib.BBANDS(df["Adj Close"], timeperiod=20)
#     bbands_talib = pd.DataFrame(index=df.index,
#                                 data={"bb_low": lower,
#                                     "bb_ma": middle,
#                                     "bb_high": upper})
#     return bbands_talib

def bollinger_strategy(df):
    bbBuy = []
    bbSell = []
    position = False
    # print(pta.bbands())

    for (index, row), ii in zip(df.iterrows(), range(len(df.index))):
        if row['Adj Close'] < row['BBL_20_2.0']:
            if position == False :
                bbBuy.append(row['Adj Close'])
                bbSell.append(np.nan)
                position = True
            else:
                bbBuy.append(np.nan)
                bbSell.append(np.nan)
        elif row['Adj Close'] > row['BBU_20_2.0']:
            if position == True:
                bbBuy.append(np.nan)
                bbSell.append(row['Adj Close'])
                position = False #To indicate that I actually went there
            else:
                bbBuy.append(np.nan)
                bbSell.append(np.nan)
        else :
            bbBuy.append(np.nan)
            bbSell.append(np.nan)

    df['bb_Buy_Signal_price'] = bbBuy
    df['bb_Sell_Signal_price'] = bbSell
    return df

def plot_bb(df):
    ta_bbands = pta.volatility.BollingerBands(close=df["Adj Close"], 
                                            window=20, 
                                            window_dev=2)
    ta_df = df.copy()
    ta_df["bb_ma"] = ta_bbands.bollinger_mavg()
    ta_df["bb_high"] = ta_bbands.bollinger_hband()
    ta_df["bb_low"] = ta_bbands.bollinger_lband()
    ta_df["bb_high_ind"] = ta_bbands.bollinger_hband_indicator()
    ta_df["bb_low_ind"] = ta_bbands.bollinger_lband_indicator()
    ta_df["bb_width"] = ta_bbands.bollinger_wband()
    ta_df["bb_pct"] = ta_bbands.bollinger_pband()
    ta_df[["bb_low", "bb_ma", "bb_high"]].plot(title="Bolinger Bands (ta)")
    return ta_df

# ta_all_indicators_df = ta.add_all_ta_features(df, open="Open", high="High", 
#                                               low="Low", close="Close", 
#                                               volume="Volume")
# ta_all_indicators_df.shape

# pta_df = pta.bbands(df["Adj Close"], length=20, talib=False)
# (
#     pta_df[["BBL_20_2.0", "BBM_20_2.0", "BBU_20_2.0"]]
#     .plot(title="Bolinger Bands (pandas_ta)")
# )

# finta_df = TA.BBANDS(df)
# (
#     finta_df[["BB_LOWER", "BB_MIDDLE", "BB_UPPER"]]
#     .plot(title="Bolinger Bands (FinTA)")
# )