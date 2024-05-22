from backtesting import Strategy
import talib as ta

class MeanReversionBollinger(Strategy):
    lookback_period = 40
    z_score_threshold = 3

    def init(self):
        close = self.data.Close
        self.mean = self.I(ta.SMA, close, self.lookback_period)
        self.std = self.I(ta.STDDEV, close, self.lookback_period)
        self.upper_band = self.mean + self.z_score_threshold * self.std
        self.lower_band = self.mean - self.z_score_threshold * self.std

    def next(self):
        if self.data.Close[-1] > self.upper_band[-1]:
            self.sell()
        elif self.data.Close[-1] < self.lower_band[-1]:
            self.buy()