from types import NoneType
import pandas as pd
from backtesting import Backtest
from src.models.stratdata import StratData
from src.services.optimiser_strategy.optimiser import determine_optimized_strategy_indicator_values, optim_func
from src.services.strategy_service.trading_strategy_factory import load_strat

def get_strategy_with_max_result(asset:pd.DataFrame, trading_strategies, comparison__metric_name:str) -> StratData:
    strongest_strategy_stats:pd.DataFrame=pd.Series()
    strongest_bt:Backtest=None
    strongest_maximize_result:int=0
    for strat_name in trading_strategies:
        trading_strategy = load_strat(strat_name)
        bt = Backtest(asset, trading_strategy, cash=10_000, commission=.002)
        stats = bt.run() # kwargs: set parameters
        optimized_strategy_stats = determine_optimized_strategy_indicator_values(strat_name, bt)
        stats = stats if bool(type(optimized_strategy_stats)==NoneType) else optimized_strategy_stats
        if (float(stats[comparison__metric_name]) > float(strongest_maximize_result)):
            if(optim_func(stats)>-1):
                strongest_maximize_result = float(stats[comparison__metric_name])
                strongest_bt = bt
                strongest_strategy_stats = stats
    return strongest_strategy_stats, strongest_bt, strongest_maximize_result