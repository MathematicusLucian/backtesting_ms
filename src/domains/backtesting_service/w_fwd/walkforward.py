import numpy as np
import pandas as pd
import vectorbt as vbt
from src.domains.strategies.ma import simulate_all_params__MA

class Walkforward:
    def __init__(self, asset_data):
        self.asset_data = asset_data
        # self.asset_data.vbt.plot().show()
        self.rolling_in_and_out_sample_config = dict(           # 30 windows, each 2 years long, reserve 180 days for test
            n=30, 
            window_len=365 * 2, 
            set_lens=(180,), 
            left_to_right=False
        )  
        self.simulation_config = dict(                          # Backtesting Portfolio params
            init_cash=100.,                                     # 100$ initial cash
            slippage=0.001,                                     # 0.1%
            fees=0.001,                                         # 0.1%
            freq='d',
            # direction='all',  # direction='both',             # long and short
            # sl_stop=stop,                                     # Stop Loss
            # sl_trail=True,                                    # Trailing Stop Loss
        )
        self.in_sharpe = None
        self.in_best_index = None
        self.windows = np.arange(10, 50)
    
    def roll_in_and_out_samples(self, price, **kwargs):
        return price.vbt.rolling_split(**kwargs)
    
    def in_hold_sharpe(self):
        return self.wf.simulate_holding(self.in_price, **self.wf.simulation_config)
    
    def calculate_in_hold_sharpe(self):
        (self.in_price, self.in_indexes), (self.out_price, self.out_indexes) = self.wf.roll_in_and_out_samples(self.asset_data, **self.wf.rolling_in_and_out_sample_config)    
            # plot=True, trace_names=['in-sample', 'out-sample']  # .show()
        self.in_hold_sharpe = self.calculate_in_hold_sharpe()
        self.in_best_fast_windows, self.in_best_slow_windows = self.wf.best_slow_and_fast_windows(self.in_price, self.windows)    # Simulate all params for in-sample ranges

    def in_sample_length(self):
        return self.in_price.shape, len(self.in_indexes)
    
    def out_sample_length(self):
        return self.out_price.shape, len(self.out_indexes)
    
    def calculate_in_best_window_pairs(self):
        return  np.array(list(zip(self.in_best_fast_windows, self.in_best_slow_windows)))
        # pd.DataFrame(in_best_window_pairs, columns=['fast_window', 'slow_window']).vbt.plot().show()

    def simulate_all_params(self, strategy, price, windows, **kwargs):
        if(strategy == 'MA'):
            return simulate_all_params__MA(self, price, windows, **kwargs)
        return None

    def calculate_in_sharpe(self, strategy):
        return self.simulate_all_params(strategy, self.in_price, self.windows, **self.simulation_config)
    
    def calculate_out_sharpe(self, strategy):
        return self.simulate_all_params(strategy, self.out_price, self.windows, **self.simulation_config)

    def simulate_holding(self, strategy, price, **kwargs):
        in_sharpe = self.calculate_in_sharpe(strategy)
        out_sharpe = self.calculate_out_sharpe(strategy)
        pf = vbt.Portfolio.from_holding(price, **kwargs)
        out_hold_sharpe = pf.sharpe_ratio()
        return in_sharpe, out_sharpe, out_hold_sharpe