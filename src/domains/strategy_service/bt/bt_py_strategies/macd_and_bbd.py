from backtesting import Strategy
from backtesting.lib import crossover
import talib as ta
from src.strategies.bollinger import BBANDS_2
from src.strategies.macd import calculate_macd_2

class MACDandBBD(Strategy):
    MACD_short = 12 
    MACD_long = 26 
    MACD_signal = 9 
    MACD_threshold = 0
    bollinger_period = 25 
    bollinger_upper_sigma = 2
    bollinger_lower_sigma = 2 

    def init(self):
        self.macd, self.MACD_signal = self.I(calculate_macd_2, self.data.Close, self.MACD_short, self.MACD_long, self.MACD_signal)
        self.bollinger_upper_sigma, self.bollinger_lower_sigma = self.I(BBANDS_2, self.data.Close, self.bollinger_period, self.bollinger_upper_sigma, self.bollinger_lower_sigma)

    def next(self): 
        if self.macd < self.MACD_threshold and self.MACD_signal < self.MACD_threshold and crossover(self.macd, self.MACD_signal)\
            and crossover(self.data.Close, self.bollinger_upper_sigma):
            if not self.position:
                self.buy() 
        elif self.macd > self.MACD_threshold and self.MACD_signal > self.MACD_threshold and crossover(self.MACD_signal, self.macd):
            self.position.close() 

class MACDandBBD_WithShortPosition(Strategy):
    MACD_short = 12
    MACD_long = 26 
    MACD_signal = 9 
    MACD_threshold = 0
    bollinger_period = 25
    bollinger_upper_sigma = 2
    bollinger_lower_sigma = 2 

    def init(self):
        self.macd, self.MACD_signal = self.I(calculate_macd_2, self.data.Close, self.MACD_short, self.MACD_long, self.MACD_signal)
        self.bollinger_upper_sigma, self.bollinger_lower_sigma = self.I(BBANDS_2, self.data.Close, self.bollinger_period, self.bollinger_upper_sigma, self.bollinger_lower_sigma)

    def next(self): 
        if self.macd < self.MACD_threshold and self.MACD_signal < self.MACD_threshold and crossover(self.macd, self.MACD_signal)\
            and crossover(self.data.Close, self.bollinger_upper_sigma):
            if not self.position:
                self.buy() 
        elif self.macd > self.MACD_threshold and self.MACD_signal > self.MACD_threshold and crossover(self.MACD_signal, self.macd):
            if not self.position:
                self.sell()
            else:
                self.position.close()