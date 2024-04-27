import warnings
warnings.filterwarnings("ignore")
# from datetime import datetime, date
from abc import ABC, abstractmethod
# from altair import Stream
from backtesting import Strategy
# from backtesting.test import GOOG
# from backtesting.lib import crossover, plot_heatmaps, resample_apply
# import matplotlib.pyplot as plt
# import seaborn as sns
from src.strategies import *

class TradingStrategyCreator(ABC):
    @abstractmethod
    def get_trading_stategy(self):
        return "blah"

class TradingStrategy_ConcreteCreator(TradingStrategyCreator):
    def get_trading_stategy(self, targetclass):
        # params={}
        # params["n1"]=1
        # params["n2"]=200
        return globals()[targetclass]

def load_strat(strat) -> type[Strategy]:
    trading_strategy_factory = TradingStrategy_ConcreteCreator()
    return trading_strategy_factory.get_trading_stategy(strat)