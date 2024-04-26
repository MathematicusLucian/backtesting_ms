from backtesting import Strategy
import talib as ta

class AverageDirectionalMovement(Strategy):
    adx_period = 7
    adx_threshold = 15

    def init(self):
        high, low, close = self.data.High, self.data.Low, self.data.Close
        self.adx = self.I(ta.ADX, high, low, close, self.adx_period)

    def next(self):
        if self.adx[-1] > self.adx_threshold:
            if self.adx[-2] < self.adx_threshold:
                self.buy()
        else:
            self.sell()