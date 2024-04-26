from backtesting import Strategy
import talib as ta

class Stochastic_OverboughtOversold(Strategy):
    stoch_period = 14
    stoch_threshold_oversold = 45
    stoch_threshold_overbought = 80

    def init(self):
        self.slowk, self.slowd = self.I(ta.STOCH, self.data.High, self.data.Low, self.data.Close,
                                        fastk_period=self.stoch_period, slowk_period=self.stoch_period,
                                        slowd_period=self.stoch_period)

    def next(self):
        if self.slowk[-1] < self.stoch_threshold_oversold and self.slowk[-2] > self.stoch_threshold_oversold:
            self.buy()
        elif self.slowk[-1] > self.stoch_threshold_overbought and self.slowk[-2] < self.stoch_threshold_overbought:
            self.sell()