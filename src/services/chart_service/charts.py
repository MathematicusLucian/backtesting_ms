from datetime import date
import numpy as np
import pandas as pd
import pandas_ta as ta
from ta import momentum
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import mplfinance as mpf
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()
plt.style.use('fivethirtyeight')

def candlesticks_chart(df):
    mpf.plot(df.head(100),type='candle',style='yahoo',volume=True)

def sma_chart(pair_key, data, start_date, end_date, days_collection):
    fig, ax = plt.subplots(figsize=(14,8))
    ax.plot(data['Adj Close'], label = pair_key ,linewidth=0.6, color='blue', alpha = 0.9)
    days_collection = [2, 5, 10]
    for days in days_collection:
        days_str = f'SMA {days}'
        ax.plot(data[days_str], label=f'SMA{days}', alpha=0.2)
    ax.scatter(data.index, data['SMA Buy_Signal_price'], label='Buy', marker='^', color='green', alpha=1 )
    ax.scatter(data.index, data['SMA Sell_Signal_price'], label='Sell', marker='v', color='red', alpha=1 )
    ax.set_title(pair_key + " Price History with buy and sell signals",fontsize=10, backgroundcolor='blue', color='white')
    ax.set_xlabel(f'{start_date} - {end_date}' ,fontsize=18)
    ax.set_ylabel('Close Price INR (₨)' , fontsize=18)
    ax.legend()
    ax.grid()
    plt.tight_layout()
    plt.show()

def macd_charts(pair_key, data):
    plt.rcParams.update({'font.size': 10})
    fig, ax1 = plt.subplots(figsize=(14,8))
    fig.suptitle(pair_key, fontsize=10, backgroundcolor='blue', color='white')
    ax1 = plt.subplot2grid((14, 8), (0, 0), rowspan=8, colspan=14)
    ax2 = plt.subplot2grid((14, 12), (10, 0), rowspan=6, colspan=14)
    ax1.set_ylabel('Price in ₨')
    ax1.plot('Adj Close',data=data, label='Close Price', linewidth=0.5, color='blue')
    ax1.scatter(data.index, data['MACD_Buy_Signal_price'], color='green', marker='^', alpha=1)
    ax1.scatter(data.index, data['MACD_Sell_Signal_price'], color='red', marker='v', alpha=1)
    ax1.legend()
    ax1.grid()
    ax1.set_xlabel('Date', fontsize=8)
    ax2.set_ylabel('MACD', fontsize=8)
    ax2.plot('MACD_12_26_9', data=data, label='MACD', linewidth=0.5, color='blue')
    ax2.plot('MACDs_12_26_9', data=data, label='signal', linewidth=0.5, color='red')
    ax2.bar(data.index,'MACDh_12_26_9', data=data, label='Volume', color=data.positive.map({True: 'g', False: 'r'}),width=1,alpha=0.8)
    ax2.axhline(0, color='black', linewidth=0.5, alpha=0.5)
    ax2.grid()
    plt.show()

    # plt.figure(figsize=(14,7))
    # plt.subplot(2,1,1)
    # plt.plot(data['Close'],label='Close Price')
    # plt.title('MACD')
    # plt.legend()
    # plt.subplot(2,1,2)
    # plt.plot(data['MACD'],label='MACD Line',color='blue')
    # plt.plot(data['MACD_Signal'], label='Signal Line', color='red')
    # plt.bar(data.index, data['MACD_Diff'],label='Histogram',color='grey',alpha=0.5)
    # plt.legend()
    # plt.show()

def bollinger_chart(pair_key, data):
    fig, ax1 = plt.subplots(figsize=(14,8))
    fig.suptitle(pair_key, fontsize=10, backgroundcolor='blue', color='white')
    ax1 = plt.subplot2grid((14, 8), (0, 0), rowspan=8, colspan=14)
    ax2 = plt.subplot2grid((14, 12), (10, 0), rowspan=6, colspan=14)
    ax1.set_ylabel('Price in ₨')
    ax1.plot(data['Adj Close'],label='Close Price', linewidth=0.5, color='blue')
    ax1.scatter(data.index, data['bb_Buy_Signal_price'], color='green', marker='^', alpha=1)
    ax1.scatter(data.index, data['bb_Sell_Signal_price'], color='red', marker='v', alpha=1)
    ax1.legend()
    ax1.grid()
    ax1.set_xlabel('Date', fontsize=8)
    ax2.plot(data['BBM_20_2.0'], label='Middle', color='blue', alpha=0.35)
    ax2.plot(data['BBU_20_2.0'], label='Upper', color='green', alpha=0.35)
    ax2.plot(data['BBL_20_2.0'], label='Lower', color='red', alpha=0.35)
    ax2.fill_between(data.index, data['BBL_20_2.0'], data['BBU_20_2.0'], alpha=0.1)
    ax2.legend(loc='upper left')
    ax2.grid()
    plt.show()

def bearish_bullish_crossover(data):
    data['Bullish_Run_Start'] = (data['MACD'] > data['MACD_Signal']) & (data['MACD'].shift(1) <= data['MACD_Signal'].shift(1))
    data['Bearish_Run_Start'] = (data['MACD'] < data['MACD_Signal']) & (data['MACD'].shift(1) >= data['MACD_Signal'].shift(1))
    plt.figure(figsize=(14, 10))
    plt.subplot(2, 1, 1)
    plt.plot(data['Close'], label='Close Price')
    plt.scatter(data.index[data['Bullish_Run_Start']], data['Close'][data['Bullish_Run_Start']], marker='^', color='g', label='Start Bullish Run')
    plt.scatter(data.index[data['Bearish_Run_Start']], data['Close'][data['Bearish_Run_Start']], marker='v', color='r', label='Start Bearish Run')
    plt.title('Tesla Stock Price and MACD')
    plt.legend()
    data['Bullish_Crossover'] = (data['MACD'] > data['MACD_Signal']) & (data['MACD'].shift(1) <= data['MACD_Signal'].shift(1))
    data['Bearish_Crossover'] = (data['MACD'] < data['MACD_Signal']) & (data['MACD'].shift(1) >= data['MACD_Signal'].shift(1))
    plt.figure(figsize=(14, 10))
    plt.subplot(2, 1, 2)
    plt.plot(data['MACD'], label='MACD Line', color='blue', alpha=0.5)
    plt.plot(data['MACD_Signal'], label='Signal Line', color='red', alpha=0.5)
    plt.bar(data.index, data['MACD_Diff'], label='Histogram', color='grey', alpha=0.5)
    plt.scatter(data.index[data['Bullish_Crossover']], data['MACD'][data['Bullish_Crossover']], marker='^', color='g', label='Bullish Crossover')
    plt.scatter(data.index[data['Bearish_Crossover']], data['MACD'][data['Bearish_Crossover']], marker='v', color='r', label='Bearish Crossover')
    plt.legend()
    plt.show()