import numpy as np
import pandas as pd
import vectorbt as vbt
from src.core.asset_data_service.asset_data_service import fetch_asset_data__close
from src.domains.backtesting_service.w_fwd.walkforward import Walkforward
from src.domains.strategies.ma import simulate_best_params__MA

class Walkforward_Optimisation:
    def __init__(self, asset_data):
        self.asset_data = asset_data
        self.wf = Walkforward(asset_data)
        color_schema = vbt.settings['plotting']['color_schema']
        self.color1 = color_schema['blue']
        self.color2 = color_schema['orange']

    def simulate_best_params(self, price, best_fast_windows, best_slow_windows, **kwargs):
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
            'out_sample_median': self.out_sharpe.groupby('split_idx').median().values,
            'out_sample_test': out_test_sharpe.values
        })
        cv_results_df.vbt.plot(
            trace_kwargs=[
                dict(line_color=self.color1), dict(line_color=self.color1, line_dash='dash'), dict(line_color=self.color1, line_dash='dot'),
                dict(line_color=self.color2), dict(line_color=self.color2, line_dash='dash'), dict(line_color=self.color2, line_dash='dot')]
        ).show()

if __name__ == "__main__":
    asset_data = fetch_asset_data__close('BTC-USD')   
    strategy = 'MA'
    wfo = Walkforward_Optimisation(asset_data)
    wfo.in_sample_simulation()
    # Optimisation
    in_sharpe, out_sharpe, out_hold_sharpe = wfo.simulate_holding(strategy, wfo.wf.out_price, **wfo.simulation_config)
    out_sharpe = wfo.calculate_out_sharpe()     # Simulate all params for out-sample ranges
    out_test_sharpe = wfo.simulate_best_params(wfo.wf.out_price, wfo.wf.in_best_fast_windows, wfo.wf.in_best_slow_windows, **wfo.simulation_config)       
        # Best in-sample params ranges used to simulate out-sample ranges
    wfo.present_results(wfo.wf.in_hold_sharpe, out_hold_sharpe, out_test_sharpe)