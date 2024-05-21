import datetime
import bt
import matplotlib.pyplot as plt
import yfinance as yf

def build_strategy(weights):
    return bt.Strategy(
        'wd', 
        [bt.algos.SelectAll(), 
         bt.algos.WeighTarget(weights), 
         bt.algos.Rebalance()]
    )

def build_backtest(strategy, df, commission_model, initial_capital):
    return bt.Backtest(
        strategy,
        df,
        initial_capital=initial_capital,
        commissions=commission_model,
        integer_positions=False
    )

def create_commission_model(q, p): # p: price, q: quantity
    val = abs(q * p)
    if val > 2000:
        return 8.6
    if val > 1000:
        return 4.3
    if val > 100:
        return 1.5
    return 1.0

def add_day_of_month(df):
    added = df.copy()
    added["day_of_month"] = df.index.day
    return added

def add_weights(df, symbol):
    strategy = df[[symbol]].copy()
    strategy.loc[:] = 0                         # start with no position within the month
    strategy.loc[df.day_of_month <= 7] = -1     # short within the first week of the month
    strategy.loc[df.day_of_month >= 23] = 1     # long during the last week of the month
    return strategy

ticker = "BTC"

data = yf.download(ticker, start="2010-01-01", end=datetime.datetime.now())
data = data.rename(columns = {'Adj Close' : ticker})
data = data.drop(['Open', 'High', 'Low', 'Close', 'Volume'], axis=1)
data = add_day_of_month(data)

weights = add_weights(data, ticker)
strategy = build_strategy(weights)
backtest = build_backtest(strategy, data, create_commission_model, initial_capital = 10_000)
first_res = bt.run(backtest)
first_res.display()
# first_res.plot(figsize=(20, 10))
# first_res.plot_weights('wd', figsize=(20, 5))
# initial_sharpe = first_res['wd'].daily_sharpe
# dist = plt.hist(initial_sharpe, bins=10)
# plt.axvline(initial_sharpe, linestyle='dashed', linewidth=1)