import datetime
import numpy as np
import pandas as pd
import vectorbt as vbt

def roll_in_and_out_samples(price, **kwargs):
    return price.vbt.rolling_split(**kwargs)

def simulate_holding(price, **kwargs):
    pf = vbt.Portfolio.from_holding(price, **kwargs)
    return pf.sharpe_ratio()

def simulate_all_params(price, windows, **kwargs):
    fast_ma, slow_ma = vbt.MA.run_combs(price, windows, r=2, short_names=['fast', 'slow'])
    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)
    pf = vbt.Portfolio.from_signals(price, entries, exits, **kwargs)
    return pf.sharpe_ratio()

def get_best_index(performance, higher_better=True):
    if higher_better:
        return performance[performance.groupby('split_idx').idxmax()].index
    return performance[performance.groupby('split_idx').idxmin()].index

def get_best_params(best_index, level_name):
    return best_index.get_level_values(level_name).to_numpy()

def simulate_best_params(price, best_fast_windows, best_slow_windows, **kwargs):
    fast_ma = vbt.MA.run(price, window=best_fast_windows, per_column=True)
    slow_ma = vbt.MA.run(price, window=best_slow_windows, per_column=True)
    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)
    pf = vbt.Portfolio.from_signals(price, entries, exits, **kwargs)
    return pf.sharpe_ratio()

now = datetime.datetime.now()
before = now - datetime.timedelta(days=3)

split_kwargs = dict(  # 30 windows, each 2 years long, reserve 180 days for test
    n=30, 
    window_len=365 * 2, 
    set_lens=(180,), 
    left_to_right=False
)
pf_kwargs = dict(direction='both', freq='d')    # long and short
windows = np.arange(10, 50)
ticker = "BTC-USD"

price = vbt.YFData.download(ticker).get('Close')
print(price)

price.vbt.plot().show()