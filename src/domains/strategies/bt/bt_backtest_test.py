import datetime
import bt
import matplotlib.pyplot as plt
import yfinance as yf
from .bt_backtest_test import add_day_of_month, add_weights, build_backtest, build_strategy, commission_model

def shuffle_prices(df):
    shuffled = df.sample(frac=1)    # randomly shuffle the prices without replacement
    shuffled.index = df.index       # reset the index
    return shuffled

data = yf.download("TLT", start="2010-01-01", end=datetime.datetime.now())
data = data.rename(columns = {'Adj Close':'TLT'})
data = data.drop(['Open', 'High', 'Low', 'Close', 'Volume'], axis=1)
initial_capital = 10_000
weights = add_weights(add_day_of_month(data), 'TLT') 
strategy = build_strategy(weights) 
backtest = build_backtest(strategy, data, initial_capital, commission_model)       
first_res = bt.run(backtest)                                                      
first_res.display()
first_res.plot(figsize=(20, 10))
first_res.plot_weights('wd', figsize=(20, 5))
runs = 1000
initial_sharpe = first_res['wd'].daily_sharpe
sharpes = []

for run in range(0, runs):
    shuffled = shuffle_prices(data)           
    shuffled_with_dom = add_day_of_month(shuffled)       
    weights = add_weights(shuffled_with_dom, 'TLT')
    strategy = build_strategy(weights)            
    backtest = build_backtest(strategy, shuffled_with_dom, initial_capital, commission_model)   
    res = bt.run(backtest)                         
    sharpe = res['wd'].daily_sharpe     # accumulate sharpe ratios
    sharpes.append(sharpe)

dist = plt.hist(sharpes, bins=10)
plt.axvline(initial_sharpe, linestyle='dashed', linewidth=1)
N = sum(i > initial_sharpe for i in sharpes)
p_value = N / runs