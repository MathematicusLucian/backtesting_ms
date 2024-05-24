import numpy as np
import pandas as pd
import vectorbt as vbt
from src.domains.strategies.ma import simulate_all_params__MA

class Walkforward:
    def __init__(self, strategy, asset_data, input_number_of_days):
        self.strategy = strategy
        self.asset_data = asset_data
        self.input_number_of_days = input_number_of_days
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
    
    def roll_in_and_out_samples(self):
        return self.asset_data.vbt.rolling_split(**self.rolling_in_and_out_sample_config)
    
    def simulate_all_params(self, price):
        if(self.strategy == 'MA'):
            return simulate_all_params__MA(price, self.windows, **self.simulation_config)
        return None

    def calculate_in_sharpe(self):
        return self.simulate_all_params(self.in_price)
    
    def calculate_out_sharpe(self):
        return self.simulate_all_params(self.out_price)

    def get_best_index(self, performance, higher_better=True):
        if higher_better:
            return performance[performance.groupby('split_idx').idxmax()].index
        return performance[performance.groupby('split_idx').idxmin()].index
    
    def get_best_params(self, best_index, level_name):
        return best_index.get_level_values(level_name).to_numpy()

    def simulate_holding(self, price):
        pf = vbt.Portfolio.from_holding(price, **self.simulation_config)
        return pf.sharpe_ratio()
    
    def calculate_in_hold_sharpe(self):
        self.in_hold_sharpe = self.simulate_holding(self.in_price)
    
    def calculate_out_hold_sharpe(self):
        self.out_hold_sharpe = self.simulate_holding(self.out_price)

    def best_slow_and_fast_windows(self):
        self.in_sharpe = self.calculate_in_sharpe()
        self.in_best_index = self.get_best_index(self.in_sharpe)
        in_best_fast_windows = self.get_best_params(self.in_best_index, 'fast_window')
        in_best_slow_windows = self.get_best_params(self.in_best_index, 'slow_window')
        return in_best_fast_windows, in_best_slow_windows
    
    def in_sample_length(self):
        return self.in_price.shape, len(self.in_indexes)
    
    def out_sample_length(self):
        return self.out_price.shape, len(self.out_indexes)
    
    def calculate_in_best_window_pairs(self):
        return np.array(list(zip(self.in_best_fast_windows, self.in_best_slow_windows)))
        # pd.DataFrame(in_best_window_pairs, columns=['fast_window', 'slow_window']).vbt.plot().show()
    
    def in_sample_simulation(self):
        (self.in_price, self.in_indexes), (self.out_price, self.out_indexes) = self.roll_in_and_out_samples()    
            # plot=True, trace_names=['in-sample', 'out-sample']  # .show()
        self.calculate_in_hold_sharpe()
        self.in_best_fast_windows, self.in_best_slow_windows = self.best_slow_and_fast_windows()    # Simulate all params for in-sample ranges