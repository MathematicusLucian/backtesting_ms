import warnings
warnings.filterwarnings("ignore")
from abc import ABC, abstractmethod
from backtesting import Strategy, Backtest
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