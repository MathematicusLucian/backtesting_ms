import sys
# sys.path.append("..")
from streamlit.web import cli as stcli
from streamlit import runtime
from src.presentation.webapp import main
from src.persistence.yf import import_data
from src.domains.strategy_service.strategy_service import *
from src.domains.strategy_service.w_fwd.walkforward import *
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