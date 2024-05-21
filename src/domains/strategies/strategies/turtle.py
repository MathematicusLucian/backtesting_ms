from backtesting import Strategy
import talib as ta
    
class Turtle(Strategy): 
    entry_lookback = 10
    exit_lookback = 20

    def init(self):
        self.high_high = self.I(ta.MAX, self.data.High, self.entry_lookback)
        self.low_low = self.I(ta.MIN, self.data.Low, self.entry_lookback)
        self.position_entered = False

    def next(self):
        if not self.position_entered:
            if self.data.Close[-1] > self.high_high[-2]:
                self.buy()
                self.position_entered = True
            elif self.data.Close[-1] < self.low_low[-2]:
                self.sell()
                self.position_entered = True
        else:
            if len(self.data) >= self.trades[0].entry_bar + self.exit_lookback:
                if self.data.Close[-1] < self.low_low[-2] or self.data.Close[-1] > self.high_high[-2]:
                    self.position.close()
                    self.position_entered = False