import numpy as np
import pandas as pd
import vectorbt as vbt
from src.core.asset_data_service.asset_data_service import fetch_asset_data__close
from src.domains.strategies.ma import simulate_all_params__MA, simulate_best_params__MA

class Walkforward:
    def __init__(self):
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
    
    def roll_in_and_out_samples(self, price, **kwargs):
        return price.vbt.rolling_split(**kwargs)

    def calculate_in_sharpe(self):
        return self.simulate_all_params(in_price, windows, **self.simulation_config)
    
    def calculate_out_sharpe(self):
        return self.simulate_all_params(out_price, windows, **self.simulation_config)

    def simulate_holding(self, price, **kwargs):
        pf = vbt.Portfolio.from_holding(price, **kwargs)
        return pf.sharpe_ratio()

    def simulate_all_params__MA(self, price, windows, **kwargs):
        return simulate_all_params__MA(self, price, windows, **kwargs)

    def simulate_best_params__MA(self, price, best_fast_windows, best_slow_windows, **kwargs):
        return simulate_best_params__MA(price, best_fast_windows, best_slow_windows, **kwargs)

    def get_best_index(self, performance, higher_better=True):
        if higher_better:
            return performance[performance.groupby('split_idx').idxmax()].index
        return performance[performance.groupby('split_idx').idxmin()].index

    def best_slow_and_fast_windows(self, in_price, windows):
        self.in_sharpe = self.calculate_in_sharpe()
        self.in_best_index = self.get_best_index(self.in_sharpe)
        in_best_fast_windows = self.get_best_params(self.in_best_index, 'fast_window')
        in_best_slow_windows = self.get_best_params(self.in_best_index, 'slow_window')
        return in_best_fast_windows, in_best_slow_windows

    def get_best_params(self, best_index, level_name):
        return best_index.get_level_values(level_name).to_numpy()
    
    def present_results(self, in_hold_sharpe, out_hold_sharpe, out_test_sharpe):
        cv_results_df = pd.DataFrame({
            'in_sample_hold': in_hold_sharpe.values,
            'in_sample_median': self.in_sharpe.groupby('split_idx').median().values,
            'in_sample_best': self.in_sharpe[self.in_best_index].values,
            'out_sample_hold': out_hold_sharpe.values,
            'out_sample_median': out_sharpe.groupby('split_idx').median().values,
            'out_sample_test': out_test_sharpe.values
        })
        color_schema = vbt.settings['plotting']['color_schema']
        cv_results_df.vbt.plot(
            trace_kwargs=[
                dict(line_color=color_schema['blue']),
                dict(line_color=color_schema['blue'], line_dash='dash'),
                dict(line_color=color_schema['blue'], line_dash='dot'),
                dict(line_color=color_schema['orange']),
                dict(line_color=color_schema['orange'], line_dash='dash'),
                dict(line_color=color_schema['orange'], line_dash='dot')
            ]
        ).show()

if __name__ == "__main__":
    wf = Walkforward()
    windows = np.arange(10, 50)
    price = fetch_asset_data__close('BTC-USD')   
        # price.vbt.plot().show()
    (in_price, in_indexes), (out_price, out_indexes) = wf.roll_in_and_out_samples(price, **wf.rolling_in_and_out_sample_config)     # plot=True, trace_names=['in-sample', 'out-sample']  # .show()
        # print(in_price.shape, len(in_indexes))        # in-sample
        # print(out_price.shape, len(out_indexes))      # out-sample
    in_hold_sharpe = wf.simulate_holding(in_price, **wf.simulation_config)
    in_best_fast_windows, in_best_slow_windows = wf.best_slow_and_fast_windows(in_price, windows)                                   # Simulate all params for in-sample ranges
        # in_best_window_pairs = np.array(list(zip(in_best_fast_windows, in_best_slow_windows)))
        # pd.DataFrame(in_best_window_pairs, columns=['fast_window', 'slow_window']).vbt.plot().show()
    out_hold_sharpe = wf.simulate_holding(out_price, **wf.simulation_config)
    out_sharpe = wf.calculate_out_sharpe()                                                                                          # Simulate all params for out-sample ranges
    out_test_sharpe = wf.simulate_best_params(out_price, in_best_fast_windows, in_best_slow_windows, **wf.simulation_config)        # Best in-sample params ranges used to simulate out-sample ranges
    wf.present_results(in_hold_sharpe, out_hold_sharpe, out_test_sharpe)