from backtesting import Strategy
import talib as ta

class MeanReversion(Strategy):
    lookback_period = 21
    z_score_threshold = 3.0
    
    def init(self):
        close = self.data.Close
        self.mean = self.I(ta.SMA, close, self.lookback_period)
        self.std = self.I(ta.STDDEV, close, self.lookback_period)

    def next(self):
        z_score = (self.data.Close[-1] - self.mean[-1]) / self.std[-1]
        if z_score > self.z_score_threshold:
            self.sell()
        elif z_score < -self.z_score_threshold:
            self.buy()