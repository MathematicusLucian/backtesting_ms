import importlib
from backtesting import Strategy
from backtesting.lib import crossover
import talib as ta
import pandas as pd
from backtesting.lib import crossover

class SuperStrategy:
    def setdata(self, sdata):
        df = pd.DataFrame(
            data={'Open': sdata.Open, 
                'High': sdata.High,
                'Low': sdata.Low,
                'Close':  sdata.Close,
                }
        )
        print(df.head())
        print(df.count())

class RsiOscillator(Strategy, SuperStrategy):
    upper_bound=60
    lower_bound=40
    rsi_window=12
    atr_window=14
    atr_stoploss=4
    atr_takeprofit=8

    def init(self):
        # param 1 --- function to calculate indicator values
        # param 2 --- pass data
        self.rsi = self.I(ta.rsi, self.data.Close, self.rsi_window)
        self.atr = self.I(ta.ATR, self.data.High , self.data.Low, self.data.Close, self.atr_window)
        self.setdata(self.data)

    def next(self):
        if self.position:
            price = self.trades[-1].entry_price
            if self.data.Low[-1] > price + (self.atr[-1] * self.atr_takeprofit) or\
                self.data.Low[-1] < price - (self.atr[-1] * self.atr_stoploss):
                if self.data.Low[-1] > price + (self.atr[-1] * self.atr_takeprofit):
                    print("take profit  " + str(self.data.index[-1]) + "  " +
                    str(price) + "  " + str(price + (self.atr[-1] * self.atr_takeprofit)))
                if self.data.Low[-1] < price - (self.atr[-1] * self.atr_stoploss):
                    print("stop loss  " + str(self.data.index[-1]) + "  " +
                    str(price) + "  " + str(price - (self.atr[-1] * self.atr_stoploss)))
                self.position.close()
            elif crossover(self.upper_bound, self.rsi):
                print("RSI close " + str(self.data.index[-1]))
                self.position.close()
        elif crossover(self.lower_bound, self.rsi):
            if not self.position:
                self.buy() 