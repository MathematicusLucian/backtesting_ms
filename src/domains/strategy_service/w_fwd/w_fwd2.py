import datetime
import numpy as np
import pandas as pd
from regex import R
import scipy.stats as stats
import kaleido
from itertools import combinations, product
import functools
import talib as ta
import vectorbt as vbt
from src.core.asset_data_service.asset_data_service import fetch_asset_data__close
# https://vectorbt.dev/api/indicators/basic/#vectorbt.indicators.basic.MACD.run
# vbt.settings.plotting["layout"]["template"] = "vbt_dark"
# vbt.settings.plotting["layout"]["width"] = 1200
# vbt.settings.plotting['layout']['height'] = 500
# vbt.settings.wrapping["freq"] = "1d"
# vbt.settings.portfolio['size_granularity'] = 1
# vbt.settings.portfolio['init_cash'] = 10000

class WalkForward:
    def __init__(self, **setup_kwargs):
        self.days = setup_kwargs['days_window']
        self.ticker = setup_kwargs['ticker']
        self.past_date, self.now = self.calculate_days_window(self.days)
        self.asset_data = fetch_asset_data__close(setup_kwargs['ticker'])        # asset_data.vbt.plot().show()
        self.split_kwargs = setup_kwargs['split_kwargs']
        self.pf_kwargs = setup_kwargs['pf_kwargs']
        (self.in_price, self.in_indexes), (self.out_price, self.out_indexes) = self.in_out_samples()
        # print(self.in_price.shape, len(self.in_indexes))                          # In-sample
        # print(self.out_price.shape, len(self.out_indexes))                        # Out-sample
        self.fast_windows, self.slow_windows, self.signal_windows = vbt.utils.params.create_param_combs(       # Define hyper-parameter space -> 49 fast x 49 slow x 19 signal. 
            (product, (combinations, np.arange(10, 40, 1), 2), np.arange(10, 21, 1))                           # To Add: X 2 macd_ewm (np.array([True, False], dtype=bool))
        )

    def roll_in_and_out_samples(self, price, **kwargs):
        return price.vbt.rolling_split(**kwargs)

    def calculate_days_window(self, days):
        now = datetime.datetime.now()
        past_date = now - datetime.timedelta(days=days)
        return past_date, now

    def get_best_index(self, performance, higher_better=True):                      # Max performance (Sharpe Ratio) by each split
        if higher_better:
            return performance[performance.groupby('split_idx').idxmax()].index
        return performance[performance.groupby('split_idx').idxmin()].index

    def get_best_params(self, best_index, level_name):
        return best_index.get_level_values(level_name).to_numpy()

    def calculate_in_sample_hyperparameters(self):
        window_list = ['macd_fast_window', 'macd_slow_window', 'macd_signal_window']
        return dict(map(lambda sub: (sub, self.get_best_params(self.in_best_index, sub)), window_list))
        
    def calculate_best_window_hyperparameters(self):
        in_best_fast_windows = self.in_best_windows['macd_fast_window']
        in_best_slow_windows = self.in_best_windows['macd_slow_window']
        in_best_signal_windows = self.in_best_windows['macd_signal_window']
        return np.array(list(zip(in_best_fast_windows, in_best_slow_windows, in_best_signal_windows)))

    def sharpe_plot(self, in_sample_pf):
        fig = in_sample_pf.sharpe_ratio().vbt.volume(                               # 3D Plot
            x_level='macd_fast_window',
            y_level='macd_slow_window',
            z_level='macd_signal_window',
            slider_level='split_idx',
            trace_kwargs=dict(
                colorbar=dict(
                    title='Sharpe Ratio', 
                )
            )
        )
        fig.show()

    def in_out_samples(self):
        return self.roll_in_and_out_samples(self.asset_data, **self.split_kwargs)
    
    def best_combinations(self, k):
       return self.in_best_index[:k]                                                # First k best combinations
    
    def first_best_combination_stats(in_sample_pf):                                 # Stats of the first best combination
        return in_sample_pf[(13, 31, 10, 0)].stats() # out_test_pf[(33, 35, 20, 19)].stats())
    
    def get_trades(in_sample_pf):                                                   # Get Trades
        return in_sample_pf[(13, 31, 10, 0)].trades.records # out_test_pf[(33, 35, 20, 19)].stats())
    
    def trades_plot(in_sample_pf):
        in_sample_pf[(13, 31, 10, 0)].trades.plot().show()  # (33, 35, 20, 19)].trades.plot().show()

    def fetch_sample(self, price):
        if(price=='in_price'):
            return self.in_price
        elif(price=='out_price'):
            return self.out_price
    
    def best_window_hyperparameters(self):
        return self.calculate_best_window_hyperparameters()
        # pd.DataFrame(best_window_hyperparameters, columns=['fast_window', 'slow_window', 'signal_window']).vbt.plot().show()
        # print(self.best_combinations(in_best_index, 5))

    def simulate_holding(price, **kwargs):                                              # Simulate buy-and-hold function
        pf = vbt.Portfolio.from_holding(price, **kwargs)
        return pf.sharpe_ratio()

    def in_hold_sharpe(self):
        return self.simulate_holding(self.in_price, **self.pf_kwargs)                   # In-sample Sharpe Ratio with buy-and-hold

    def out_hold_sharpe(self):
        return self.simulate_holding(self.out_price, **self.pf_kwargs)                  # Out-sample Sharpe Ratio with buy-and-hold

    def simulate_holding(self, price, **kwargs):
        pf = vbt.Portfolio.from_holding(price, **kwargs)
        return pf.sharpe_ratio()

    def get_best_index(self, performance, higher_better=True):
        if higher_better:
            return performance[performance.groupby('split_idx').idxmax()].index
        return performance[performance.groupby('split_idx').idxmin()].index

    def get_best_params(self, best_index, level_name):
        return best_index.get_level_values(level_name).to_numpy()
    
    def sma_cross(self, close, slow_period, fast_period):
        close = vbt.nb.ffill_1d_nb(close)           # Fix our Data
        slow_ma = ta.SMA(close, slow_period)        # Calculate Moving Averages
        fast_ma = ta.SMA(close, fast_period)
        # Calculate Signals
        long_entry = vbt.nb.crossed_above_1d_nb(fast_ma, slow_ma)
        short_entry = vbt.nb.crossed_below_1d_nb(fast_ma, slow_ma)
        trend = fast_ma > slow_ma
        return long_entry, short_entry, trend
    
    def build_stategy(self):
        return vbt.IF(
            class_name='strat',
            short_name='strat',
            input_names=['close'],
            param_names=['slow_period', 'fast_period'],
            output_names=['long_entry', 'short_entry', 'trend']
        ).with_apply_func(
            self.sma_cross,
            takes_1d=True,
            slow_period=200,
            fast_period=50
        )
    
    def perf(self, data, ind, pos_size, metric='sharpe_ratio'):
        pf = vbt.Portfolio.from_signals(
            self.asset_data,
            entries=ind.long_entry,
            short_entries=ind.short_entry,
            size=pos_size,
            size_type='amount'
        )
        return getattr(pf, metric)
    
    def split_func(self, splits, bounds, index, length_IS=20, length_OOS=30):
        if len(splits) == 0:
            new_split = (slice(0, length_IS), slice(length_IS, length_OOS+length_IS))
        else:
            # Previous split, second set, right bound
            prev_end = bounds[-1][1][1]
            # Split Calculation
            new_split = (
                slice(prev_end-length_IS, prev_end),
                slice(prev_end, prev_end + length_OOS)
            )
        if new_split[-1].stop > len(index):
            return None
        return new_split
    
    def run_strategy(self):
        strat = self.build_stategy()
        sma_strat = strat.run(
            self.asset_data,
            slow_period=np.arange(40, 150, 10, dtype=int),
            fast_period=np.arange(10, 35, 5, dtype=int),
            param_product=True
        )
        pos_size = self.get_fx_position_size(self.asset_data, init_cash=10_000, risk=0.02)
        pf = vbt.Portfolio.from_signals(
            self.asset_data,
            entries=sma_strat.long_entry,
            short_entries=sma_strat.short_entry,
            size=pos_size,
            size_type='amount'
        )
        stats_df = pf.stats([
            'total_return', 
            'total_trades', 
            'win_rate', 
            'expectancy'
        ], agg_func=None)
        stats_df.groupby(('symbol'))['Expectancy'].idxmax()
        d_IS, d_OOS, _ = self.get_optimized_split(len(self.asset_data.close.index), 0.75, 10)
        print(d_IS, d_OOS)
        splitter = vbt.Splitter.from_split_func(
                self.asset_data.close.index,
                self.split_func,
                split_args=(
                    vbt.Rep("splits"),
                    vbt.Rep("bounds"),
                    vbt.Rep("index"),
                ),
                split_kwargs={
                    'length_IS':d_IS,
                    'length_OOS':d_OOS
                },
                set_labels=["IS", "OOS"]
        )
        fig = splitter.plot()
        fig.show()
        #fig.write_html('wfo.html', full_html=False)
        train_perf = splitter.apply(
            self.perf,
            vbt.Takeable(self.asset_data),
            vbt.Takeable(sma_strat),
            vbt.Takeable(pos_size),
            metric='sharpe_ratio',
            _execute_kwargs=dict(  
                show_progress=False,
                clear_cache=50,  
                collect_garbage=50
            ),
            set_='IS',
            merge_func='concat',
            execute_kwargs=dict(show_progress=True),
        )
        print(train_perf)
        best = train_perf.groupby(['split', 'symbol']).idxmax()
        best[:] = [(i[1], i[2], i[3]) for i in best]
        print(best)
        optimized_long_entry = []
        optimized_short_entry = []
        for i in best.index.get_level_values('split').unique():
            _opt_long = splitter['OOS'].take(sma_strat.long_entry)[i][best[i]].droplevel(['strat_slow_period', 'strat_fast_period'], axis=1)
            _opt_short = splitter['OOS'].take(sma_strat.short_entry)[i][best[i]].droplevel(['strat_slow_period', 'strat_fast_period'], axis=1)

            optimized_long_entry.append(_opt_long)
            optimized_short_entry.append(_opt_short)
        optimized_long_entry = pd.concat(optimized_long_entry)
        optimized_short_entry = pd.concat(optimized_short_entry)
        pf = vbt.Portfolio.from_signals(
            self.asset_data,
            entries=optimized_long_entry,
            short_entries=optimized_short_entry,
            size=pos_size,
            size_type='amount',
            group_by=[0]*len(self.asset_data.close.columns)
        )
        fig = pf.plot(settings=dict(bm_returns=True))
        fig.show()

    def simulate_all_params(self, price, windows, **kwargs):
        fast_ma, slow_ma = vbt.MA.run_combs(price, windows, r=2, short_names=['fast', 'slow'])
        entries = fast_ma.ma_crossed_above(slow_ma)
        exits = fast_ma.ma_crossed_below(slow_ma)
        pf = vbt.Portfolio.from_signals(price, entries, exits, **kwargs)
        return pf.sharpe_ratio()

    def simulate_best_params(self, price, best_fast_windows, best_slow_windows, **kwargs):
        fast_ma = vbt.MA.run(price, window=best_fast_windows, per_column=True)
        slow_ma = vbt.MA.run(price, window=best_slow_windows, per_column=True)
        entries = fast_ma.ma_crossed_above(slow_ma)
        exits = fast_ma.ma_crossed_below(slow_ma)
        pf = vbt.Portfolio.from_signals(price, entries, exits, **kwargs)
        return pf.sharpe_ratio()

    def run_MACD_sim__all_params(self, sample_type):
        macd_ind = vbt.MACD.run(sample_type, fast_window=self.fast_windows, slow_window=self.slow_windows, signal_window=self.signal_windows)    # Run MACD indicator
        # entries = macd_ind.macd_above(0) & macd_ind.macd_above(macd_ind.signal)           # Entry when MACD is above zero AND signal
        # exits = macd_ind.macd_below(0) | macd_ind.macd_below(macd_ind.signal)             # Exit when MACD is below zero OR signal
        # return vbt.Portfolio.from_signals(sample_type, entries, exits, **self.pf_kwargs)   
    
    def wfwd_sim__in_and_out_sample(self, strategy):                                        # Simulation with both in/out_samples
        if(strategy=='MACD'):
            self.in_sample_pf = self.run_MACD_sim__all_params('in_price')
            # self.out_sample_pf = self.run_MACD_sim__all_params(self.fetch_sample('out-price'), self.fast_windows, self.slow_windows, self.signal_windows, **self.pf_kwargs)
            # self.in_best_index = self.get_best_index(self.in_sample_pf.sharpe_ratio())
            # self.in_best_windows = self.calculate_in_sample_hyperparameters()

    def wfwd_sim__best_params(self, sample_type, strategy):                                       # Run MACD indicator
        self.wfwd_sim__in_and_out_sample(strategy)
        # if(strategy=='MACD'):
            # Use best params from in-sample ranges -> simulate for out-sample ranges
            # macd_ind = vbt.MACD.run(self.fetch_sample(sample_type), fast_window=self.in_best_windows['macd_fast_window'], slow_window=self.in_best_windows['macd_slow_window'], signal_window=self.in_best_windows['macd_signal_window'], per_column=True)   # per_column=True for one combination per column
            # entries = macd_ind.macd_above(0) & macd_ind.macd_above(macd_ind.signal)         # Long when MACD is above zero AND signal
            # exits = macd_ind.macd_below(0) | macd_ind.macd_below(macd_ind.signal)           # Short when MACD is below zero OR signal
            # self.out_test_pf = vbt.Portfolio.from_signals(self.fetch_sample(sample_type), entries, exits, **self.pf_kwargs)

    def results_df(self):
        return pd.DataFrame({
            'in_sample_hold': self.in_hold_sharpe.values,
            'in_sample_median': self.in_sample_pf.sharpe_ratio().groupby('split_idx').median().values,
            'in_sample_best': self.in_sample_pf.sharpe_ratio()[self.in_best_index].values,
            'out_sample_hold': self.out_hold_sharpe.values,
            'out_sample_median': self.out_sample_pf.sharpe_ratio().groupby('split_idx').median().values,
            'out_sample_test': self.out_test_pf.sharpe_ratio().values
        })
    
    def plot_results(self):
        color_schema = vbt.settings['plotting']['color_schema']
        self.results_df.vbt.plot(
            trace_kwargs=[
                dict(line_color=color_schema['blue']),
                dict(line_color=color_schema['blue'], line_dash='dash'),
                dict(line_color=color_schema['blue'], line_dash='dot'),
                dict(line_color=color_schema['orange']),
                dict(line_color=color_schema['orange'], line_dash='dash'),
                dict(line_color=color_schema['orange'], line_dash='dot')
            ]
        ).show()