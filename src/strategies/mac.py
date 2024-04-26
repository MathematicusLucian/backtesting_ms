from backtesting import Strategy
from backtesting.lib import crossover
import talib as ta

class MovingAverageCrossover(Strategy):
    short_period = 50
    long_period = 200

    def init(self):
        close = self.data.Close
        self.short_ma = self.I(ta.SMA, close, self.short_period)
        self.long_ma = self.I(ta.SMA, close, self.long_period)

    def next(self):
        if crossover(self.short_ma, self.long_ma):
            self.buy()
        elif crossover(self.long_ma, self.short_ma):
            self.sell()