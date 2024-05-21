from backtesting import Strategy
from backtesting.lib import resample_apply
from src.strategies.multi_timeframes import RSI, SMA

class System(Strategy):
    d_rsi = 30
    w_rsi = 30
    level = 70
    
    def init(self):
        self.ma10 = self.I(SMA, self.data.Close, 10)
        self.ma20 = self.I(SMA, self.data.Close, 20)
        self.ma50 = self.I(SMA, self.data.Close, 50)
        self.ma100 = self.I(SMA, self.data.Close, 100)
        self.daily_rsi = self.I(RSI, self.data.Close, self.d_rsi)  # Compute daily RSI(30)
        # To construct weekly RSI, we can use `resample_apply()` helper function from the library
        self.weekly_rsi = resample_apply(
            'W-FRI', RSI, self.data.Close, self.w_rsi)
        
    def next(self):
        price = self.data.Close[-1]
        # If we don't already have a position, and if all conditions are satisfied, enter long.
        if (not self.position and
            self.daily_rsi[-1] > self.level and
            self.weekly_rsi[-1] > self.level and
            self.weekly_rsi[-1] > self.daily_rsi[-1] and
            self.ma10[-1] > self.ma20[-1] > self.ma50[-1] > self.ma100[-1] and
            price > self.ma10[-1]):
            # Buy at market price on next open, but do set 8% fixed stop loss.
            self.buy(sl=.92 * price)
        # If the price closes 2% or more below 10-day MA close the position, if any.
        elif price < .98 * self.ma10[-1]:
            self.position.close()

# System
# backtest = Backtest(GOOG, System, commission=.002)
# backtest.run()
# backtest.optimize(d_rsi=range(10, 35, 5),
#                   w_rsi=range(10, 35, 5),
#                   level=range(30, 80, 10))
# backtest.plot()