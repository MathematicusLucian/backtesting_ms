import os
import vectorbt as vbt
import yfinance as yf
import pandas as pd
import pandas_ta as ta

def read_asset_data(ticker):
    return vbt.YFData.download(ticker)
    # return vbt.YFData.download(
    #     ticker, 
    #     missing_index='drop',
    #     start=before.timestamp(),
    #     end=now.timestamp()
    # )

def import_data():
    df = pd.DataFrame()
    cac_df = df.ta.ticker(
        "^FCHI", start="2020-01-01", end="2022-01-01", timeframe="1d", limit=10000
    )
    cac_df.drop(labels=["Dividends", "Stock Splits"], axis=1, inplace=True)
    # print(cac_df.loc[cac_df["Volume"] == 0])
    # cac_df.to_csv("data.csv")
    return cac_df

def fetch_data(ticker):
    base_path = os.getcwd()
    return pd.read_csv(f"{base_path}/src/persistence/mock/data.csv", index_col=0, parse_dates=True)