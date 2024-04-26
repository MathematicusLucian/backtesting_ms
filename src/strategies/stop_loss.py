import pandas as pd
import talib as ta
import numpy as np
from backtesting import Strategy
from backtesting.lib import TrailingStrategy

class StopLossFix(Strategy):
    def init(self):
        pass

    def next(self): 
        if self.position:
            pass
        else:
            price = self.data.Close[-1]
            self.buy(tp = price + 50, sl = price - 10)

class StopLoss_ATR(Strategy):
    n = 14

    def ATR_Backtesting(self, phigh, plow, pclose, period):
        high = pd.Series(phigh)
        low = pd.Series(plow)
        close = pd.Series(pclose)
        return ta.ATR(\
            np.array(high).astype("double"),\
            np.array(low).astype("double"),\
            np.array(close).astype("double"),\
            timeperiod=period)

    def init(self):
        self.atr = self.I(self.ATR_Backtesting, self.data.High, self.data.Low, self.data.Close, self.n)

    def next(self): 
        if self.position:
            pass
        else:
            price = self.data.Close[-1]
            self.buy(tp = price + self.atr * 2.5, sl = price - self.atr * 2.5)

class StopLoss_Trailing(TrailingStrategy):
    def init(self):
        super().init()
        super().set_trailing_sl(2)
        pass

    def next(self): 
        super().next()
        if self.position:
            pass
        else:
            price = self.data.Close[-1]
            self.buy(tp = price + 50)

class StopLoss_Percentage(Strategy):
    def init(self):
        pass

    def next(self): 
        super().next()
        if self.position:
            pass
        else:
            price = self.data.Close[-1]
            self.buy(tp = price + 50)