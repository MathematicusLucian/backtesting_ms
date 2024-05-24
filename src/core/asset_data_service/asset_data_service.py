from src.persistence.yf import read_asset_data

def fetch_asset_data(ticker):
    # cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    return read_asset_data(ticker).data[ticker] #.get(cols) 

def fetch_asset_data__close(ticker):
    return read_asset_data(ticker).get('Close') 

def crypto_currencies():
    return ["BTC", "ETH", "SOL", "PEPE", "BONK"]

def trad_currencies():
    return ["GBP", "USD"]