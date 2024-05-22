import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr

def get_asset_data(asset, start, end) -> pd.DataFrame:
    asset_df:pd.DataFrame = pdr.get_data_yahoo(asset, start=start, end=end) 
    asset_df["Date"] = pd.to_datetime(asset_df.index) 
    return asset_df

def append_row(df, row):
    return pd.concat([
            df, 
            pd.DataFrame([row], columns=row.index)
        ]).reset_index(drop=True)

def save_to_csv(df, file_name):
    df.to_csv(f'./results/{file_name}.csv', sep=',', index=False, encoding='utf-8')