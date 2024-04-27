from datetime import date
import pandas as pd
from backtesting import Backtest
from src.services.config_service.config import Configuration
from src.services.strategy_service.trading_strategy_factory import *

if __name__ == "__main__":
    conf = Configuration.load_json('strategies_config.json')
    trading_strategies = conf.trading_strategies
    strategy_results_columns = tuple(conf.strategy_results_columns)
    asset_df:pd.DataFrame = get_asset_data("BTC-GBP", date(2014,1,1), date.today())
    maximize_metric_name:str = "Win Rate [%]"
    strongest_strategy_stats:pd.DataFrame=None
    strongest_bt:Backtest=None
    strongest_maximize_result:int=0
    
    # Backtest to calculate strongest strat
    strongest_strategy_stats, strongest_bt, strongest_maximize_result = get_strategy_with_max_result(asset_df, trading_strategies, maximize_metric_name)
    print(f"\n\nStrongest Strat: {strongest_strategy_stats['_strategy']}", f"\nResult:{strongest_maximize_result}\n")

    # Save results to CSV files
    strongest_strat_df:pd.DataFrame = append_row(pd.DataFrame(columns=strategy_results_columns), strongest_strategy_stats) \
        .reindex(columns=strategy_results_columns)
    list(map(save_to_csv, 
        (strongest_strat_df, strongest_strategy_stats["_equity_curve"], strongest_strategy_stats["_trades"]), 
        ("strongest_strat", "strongest_strat__equity_curve", "strongest_strat__trades"))
    )
    # Plot chart
    strongest_bt.plot(plot_volume=False, plot_pl=False, filename='plots/strongest_strat.html')