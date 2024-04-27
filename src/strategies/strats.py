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
plt.style.use('fivethirtyeight')
from src.services.chart_service.charts import *
from src.strategies import bollinger, ema, macd, rsi, sma

# stock_pairs_keys = ['BTC-GBP', 'ETH-GBP', 'SOL-GBP']
# signals = ['Buy_Signal_price', 'Sell_Signal_price']
# days_collection = [2, 5, 10, 30, 50, 100, 200]
# base="USD"
# second_currency="BTC"
# period="1yr"
# fast=12
# slow=26
# signal=9
# start_date = date(2017,8,4)
# end_date = date.today()
# df_history = get_history(stock_pairs_keys, start_date, end_date)
# stock_pairs_dict = get_stock_pairs(df_history, stock_pairs_keys)
# pair_key = 'ETH-GBP'
# pair_data = stock_pairs_dict[pair_key]

# for pair_name in stock_pairs_dict:
#     # --- Candlesticks ---
#     # candlesticks_chart(pair_data)

#     # --- SMA ---
#     data = stock_pairs_dict[pair_name]
#     df_sma = sma.calculate_sma(data, days_collection)
#     df_sma = sma.sma_strategy(df_sma, signals)
#     sma_chart(pair_name, df_sma, start_date, end_date, days_collection)

#     # --- MACD ---
#     # pair_data: pd.DataFrame = macd.calculate_macd(pair_data)
#     # df_macd_strategy_outcome = macd.macd_strategy(pair_data, 0.025)
#     # macd_charts(pair_key, df_macd_strategy_outcome)

#     # --- Bollinger ---
#     # pair_data = bollinger.calculate_bollinger(df_macd_strategy_outcome)
#     # df_bollinger_strategy_outcome = bollinger.bollinger_strategy(pair_data)
#     # bollinger_chart(pair_key, df_bollinger_strategy_outcome)