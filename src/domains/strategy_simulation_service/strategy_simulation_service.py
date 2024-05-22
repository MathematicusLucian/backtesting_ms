import vectorbt as vbt
import pandas as pd
from src.persistence.yf import read_asset_data
from src.domains.strategies import strategies_functions_dict

class StrategySimService:
    def __init__(self):
        self.asset_data = {}

    def fetch_data(self, ticker):
        asset_data = read_asset_data(ticker).data[ticker]
        self.asset_data = pd.DataFrame.from_dict(asset_data, orient='columns') # orient='index', columns=asset_data_cols)
        # asset_data_cols = ['Open','High','Low','Close','Volume','Dividends','Stock Splits']
        # asset_data.columns = asset_data_cols
        # asset_data.columns = set(k.lower() for k in asset_data.columns)

    def calc_indicators(self, ticker, indicator, dict_indicators):
        dict_indicators_columns = {"open_", "high", "low", "close", "volume"}
        for i in dict_indicators:                                   # Replace value with data[value]
            if i in dict_indicators_columns:
                col_name = i.title().rstrip("_")
                dict_indicators[i] = self.asset_data[col_name]
        TA = vbt.IndicatorFactory.from_pandas_ta(indicator)         # pandas-ta indicator
        return TA.run(**dict_indicators)

    def run_strategies(self, init_cash, asset, asset_base, indicator, dict_indicators):
        ticker = f"{asset}-{asset_base}"
        self.fetch_data(ticker)
        ta = self.calc_indicators(ticker, indicator, dict_indicators)
        strategies_to_run = ta.output_names
        strategies_outcome = {}
        for name in strategies_to_run:
            if name in strategies_functions_dict:
                strategy_outcome = strategies_functions_dict[name](ta)
                strategies_outcome.update(strategy_outcome)
                strategies_outcome["close"] = self.asset_data["Close"]
                strategies_outcome["portfolio"] = vbt.Portfolio.from_signals(
                    strategies_outcome["close"], 
                    strategies_outcome["entries"], 
                    strategies_outcome["exits"], 
                    init_cash=init_cash
                )
            else:
                strategies_outcome["name"] = name
                strategies_outcome["name_attr"] = getattr(ta, name)
        return strategies_outcome