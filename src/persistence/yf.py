import vectorbt as vbt

def read_asset_data(ticker):
    return vbt.YFData.download(ticker)
    # return vbt.YFData.download(
    #     ticker, 
    #     missing_index='drop',
    #     start=before.timestamp(),
    #     end=now.timestamp()
    # )