import vectorbt as vbt
import pandas as pd
from src.core.asset_data_service.asset_data_service import fetch_asset_data
from src.domains.strategies import strategies_functions_dict

class StrategySimService:
    def __init__(self):
        self.asset_data = None

    def create_indicators(self, indicator, dict_indicators):
        dict_indicators_columns = {"open_", "high", "low", "close", "volume"}
        for i in dict_indicators:                                   # Replace value with data[value]
            if i in dict_indicators_columns:
                col_name = i.title().rstrip("_")
                dict_indicators[i] = self.asset_data[col_name]
        TA = vbt.IndicatorFactory.from_pandas_ta(indicator)         # pandas-ta indicator
        return TA.run(**dict_indicators)

    def run_strategies(self, asset_data, init_cash, indicator, dict_indicators):
        self.asset_data = asset_data
        ta = self.create_indicators(indicator, dict_indicators)
        strategies_outcome = {}
        for name in ta.output_names: # strategies_to_run
            if name in strategies_functions_dict:
                strategy_outcome = strategies_functions_dict[name](ta)
                strategies_outcome.update(strategy_outcome)
                strategies_outcome["close"] = self.asset_data["Close"]
                strategies_outcome["portfolio"] = vbt.Portfolio.from_signals(strategies_outcome["close"], strategies_outcome["entries"], strategies_outcome["exits"], init_cash=init_cash)
            else:
                strategies_outcome["name"] = name
                strategies_outcome["name_attr"] = getattr(ta, name)
        return strategies_outcome