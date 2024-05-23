import sys
# sys.path.append("..")
from streamlit.web import cli as stcli
from streamlit import runtime
from src.presentation.streamlit import main
# from src.persistence.yf import import_data
from src.domains.strategy_simulation_service.strategy_simulation_service import *
# from src.domains.backtesting_service.w_fwd.walkforward import *
# from src.domains.strategy_service.custom_indicators import *
# from src.domains.strategy_service.custom_functions import *

# # Setup
# setup_kwargs = dict(
#     days_window = 1000,
#     ticker = "BTC-GBP",
#     stop_loss = 0.05,                                       # 5%
#     split_kwargs = dict(                                    # WalkForward Split params - 30 windows, each 2 years long, 180 days for test
#         n=20, 
#         window_len=365 * 2, 
#         set_lens=(180,), 
#         left_to_right=False
#     ),
#     pf_kwargs = dict(                                       # Backtesting Portfolio params
#         init_cash=100.,                                     # 100$ initial cash
#         slippage=0.001,                                     # 0.1%
#         fees=0.001,                                         # 0.1%
#         freq='d',
#         # direction='both',                                 # long and short
#         # sl_stop=stop,                                     # Stop Loss
#         # sl_trail=True,                                    # Trailing Stop Loss
#     )
# )

# # Backtest
# wf = WalkForward(**setup_kwargs)
# # wf.wfwd_sim__best_params(sample_type='in_price', strategy='MACD')
# sma_strat = wf.run_strategy()

if __name__ == "__main__":
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())

# from datetime import date
# import pandas as pd
# from backtesting import Backtest
# from src.services.config_service.config import Configuration
# from src.services.strategy_service.data_logic import get_asset_data, append_row, save_to_csv
# from src.services.strategy_service.trading_strategy_factory import *
# from src.services.strategy_service.comparison import get_strategy_with_max_result

# if __name__ == "__main__":
#     conf = Configuration.load_json('strategies_config.json')
#     trading_strategies = conf.trading_strategies
#     strategy_results_columns = tuple(conf.strategy_results_columns)
#     asset_df:pd.DataFrame = get_asset_data("BTC-GBP", date(2014,1,1), date.today())
#     comparison__metric_name:str = "Win Rate [%]"
#     strongest_strategy_stats:pd.DataFrame=None
#     strongest_bt:Backtest=None
#     strongest_maximize_result:int=0
    
#     # ml() #SciKit Machine Learning
    
#     # Backtest to calculate strongest strat
#     strongest_strategy_stats, strongest_bt, strongest_maximize_result = get_strategy_with_max_result(asset_df, trading_strategies, comparison__metric_name)

#     if not bool(strongest_strategy_stats.empty):
#         print(f"\n\nStrongest Strat: {strongest_strategy_stats['_strategy']}", f"\nResult:{strongest_maximize_result}\n")

#         # Save results to CSV files
#         strongest_strat_df:pd.DataFrame = append_row(pd.DataFrame(columns=strategy_results_columns), strongest_strategy_stats) \
#             .reindex(columns=strategy_results_columns)
#         list(map(save_to_csv, 
#             (strongest_strat_df, strongest_strategy_stats["_equity_curve"], strongest_strategy_stats["_trades"]), 
#             ("strongest_strat", "strongest_strat__equity_curve", "strongest_strat__trades"))
#         )
#         # Plot chart
#         # strongest_bt.plot(plot_volume=False, plot_pl=False, filename='plots/strongest_strat.html')
#     else:
#         print("No strategy meets the optimiser conditions")