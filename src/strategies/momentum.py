from backtesting import Strategy
from backtesting.lib import resample_apply
import talib as ta

class Momentum(Strategy):
    small_threshold = 0
    large_threshold = 3
    period_long = 7
    period_short = 2

    def momentum(self, data):
        return data.pct_change(periods=7).to_numpy() * 100

    def init(self):
        self.pct_change_long = resample_apply(str(self.period_long) + "D", self.momentum, self.data.Close)
        self.pct_change_short = resample_apply(str(self.period_short) + "D", self.momentum, self.data.Close)

    def next(self): 
        change_long = self.pct_change_long[-1]
        change_short = self.pct_change_long[-1]

        if self.position:
            if self.position.is_long and change_short < self.small_threshold:
                self.position.close()
            elif self.position.is_short and change_short > -1 * self.small_threshold:
                self.position.close()
        else:
            if change_long > self.large_threshold and change_short > self.small_threshold:
                self.buy()
            elif change_long < -1 * self.large_threshold and change_short < -1 * self.small_threshold:
                self.sell()

class Momentum__Volatility(Strategy):
    lookback_period = 10
    atr_period = 15
    atr_threshold = 2.5    
    
    def init(self):
        close = self.data.Close
        self.returns = self.I(ta.MOM, close, self.lookback_period)
        self.atr = self.I(ta.ATR, self.data.High, self.data.Low, close, self.atr_period)

    def next(self):
        if self.returns[-1] > 0 and self.atr[-1] > self.atr_threshold:
            self.sell()
        elif self.returns[-1] < 0 and self.atr[-1] > self.atr_threshold:
            self.buy()