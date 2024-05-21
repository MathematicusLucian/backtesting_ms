import vectorbt as vbt

def read_asset_data(ticker):
    price = vbt.YFData.download(ticker).get('Close')
    # price = vbt.YFData.download(
    #     ticker, 
    #     missing_index='drop',
    #     start=before.timestamp(),
    #     end=now.timestamp()
    # ).get('Close')