import numpy as np
import pandas as pd
import vectorbt as vbt
from src.core.asset_data_service.asset_data_service import fetch_asset_data__close
from src.domains.backtesting_service.w_fwd.walkforward import Walkforward
from src.domains.strategies.ma import simulate_all_params__MA, simulate_best_params__MA

class Walkforward_Optimisation:
    def __init__(self, strategy, asset_data, input_number_of_days):
        self.asset_data = asset_data
        self.input_number_of_days = input_number_of_days
        self.strategy = strategy
        self.wf = Walkforward(self.strategy, self.asset_data, self.input_number_of_days)

    def in_sample_simulation(self):
        self.wf.in_sample_simulation()

    def out_sample_simulation(self):
        self.in_sharpe = self.wf.in_sharpe
        self.in_hold_sharpe = self.wf.in_hold_sharpe
        self.out_hold_sharpe = self.wf.simulate_holding(self.wf.out_price)
        self.out_sharpe = self.wf.calculate_out_sharpe()
        self.out_test_sharpe = simulate_best_params__MA(self.wf.out_price, self.wf.in_best_fast_windows, self.wf.in_best_slow_windows, **self.wf.simulation_config)

    def optimisation_results(self):
        strategies_outcome = {}
        strategies_outcome['in_sample_hold'] = self.in_hold_sharpe.values
        strategies_outcome['in_sample_median'] = self.in_sharpe.groupby('split_idx').median().values
        strategies_outcome['in_sample_best'] = self.in_sharpe[self.wf.in_best_index].values
        strategies_outcome['out_sample_hold'] = self.out_hold_sharpe.values
        strategies_outcome['out_sample_median'] = self.out_sharpe.groupby('split_idx').median().values
        strategies_outcome['out_sample_test'] = self.out_test_sharpe.values
        return strategies_outcome
    
    def optimisation_results__df(self):
        self.optimisation_results_df = pd.DataFrame({
            'in_sample_hold': self.in_hold_sharpe.values,
            'in_sample_median': self.in_sharpe.groupby('split_idx').median().values,
            'in_sample_best': self.in_sharpe[self.wf.in_best_index].values,
            'out_sample_hold': self.out_hold_sharpe.values,
            'out_sample_median': self.out_sharpe.groupby('split_idx').median().values,
            'out_sample_test': self.out_test_sharpe.values
        })
        return self.optimisation_results_df