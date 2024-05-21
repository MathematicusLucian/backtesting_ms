import datetime
import numpy as np
import pandas as pd
import scipy.stats as stats
import kaleido
from itertools import combinations, product
import vectorbt as vbt
from .funcs import *
from .macd import *
from src.core.asset_data_service.asset_data_service import fetch_asset_data

def w_fwd():
    now = datetime.datetime.now()
    before = now - datetime.timedelta(days=1000)

    ticker = "BTC-GBP"
    asset_data = fetch_asset_data(ticker).get('Close')
    # print(asset_data)
    # asset_data.vbt.plot().show()
    # asset_data.vbt.plot().show_png()

    # WalkForward Split params - 30 windows, each 2 years long, 180 days for test
    split_kwargs = dict(
        n=20, 
        window_len=365 * 2, 
        set_lens=(180,), 
        left_to_right=False
    )
    # stop_loss = 0.05  # 5%
    # Backtesting Portfolio params
    pf_kwargs = dict(
        init_cash=100.,      # 100$ initial cash
        slippage=0.001,      # 0.1%
        fees=0.001,          # 0.1%
        freq='d',
        # direction='both',  # long and short
        # sl_stop=stop,      # Stop Loss
        # sl_trail=True,     # Trailing Stop Loss
    )

    # Define hyper-parameter space -> 49 fast x 49 slow x 19 signal. To Add: X 2 macd_ewm (np.array([True, False], dtype=bool))
    fast_windows, slow_windows, signal_windows = vbt.utils.params.create_param_combs(
        (product, (combinations, np.arange(10, 40, 1), 2), np.arange(10, 21, 1))
    )

    (in_price, in_indexes), (out_price, out_indexes) =roll_in_and_out_samples(asset_data, **split_kwargs)
    print(in_price.shape, len(in_indexes))    # in-sample
    print(out_price.shape, len(out_indexes))  # out-sample

    in_pf = simulate_all_params_MACD(in_price, fast_windows, slow_windows, signal_windows, **pf_kwargs)
