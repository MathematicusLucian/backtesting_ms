import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta
from backtesting import Strategy
from backtesting import Backtest
import backtesting

def generate_grid(midprice, grid_distance, grid_range):
    return (np.arange(midprice-grid_range, midprice+grid_range, grid_distance))

class GridStrat(Strategy):
    mysize = 50
    def init(self):
        super().init()
        self.signal1 = self.I(SIGNAL)

    def next(self):
        super().next()
        slatr = 1.5*grid_distance #5*self.data.ATR[-1]
        TPSLRatio = 0.5

        if self.signal1==1 and len(self.trades)<=10000:             
            sl1 = self.data.Close[-1] + slatr
            tp1 = self.data.Close[-1] - slatr*TPSLRatio
            self.sell(sl=sl1, tp=tp1, size=self.mysize)

            sl1 = self.data.Close[-1] - slatr
            tp1 = self.data.Close[-1] + slatr*TPSLRatio
            self.buy(sl=sl1, tp=tp1, size=self.mysize)

dataF = yf.download("EURUSD=X", start="2022-11-19", end="2023-01-16", interval='5m')
#dataF.iloc[:,:]
grid_distance = 0.005
midprice = 1.065
grid = generate_grid(midprice=midprice, grid_distance=grid_distance, grid_range=0.1)
signal = [0]*len(dataF)
i=0
for index, row in dataF.iterrows():
    for p in grid:
        if min(row.Low, row.High)<p and max(row.Low, row.High)>p:
            signal[i]=1
    i+=1
dataF["signal"]=signal
dataF[dataF["signal"]==1]
dfpl = dataF[:].copy()
def SIGNAL():
    return dfpl.signal
dfpl['ATR'] = ta.atr(high = dfpl.High, low = dfpl.Low, close = dfpl.Close, length = 16)
dfpl.dropna(inplace=True)
bt = Backtest(dfpl, GridStrat, cash=50, margin=1/100, hedging=True, exclusive_orders=False)
stat = bt.run()
backtesting.set_bokeh_output(notebook=False)
bt.plot(show_legend=False, plot_width=None, plot_equity=True, plot_return=False, 
plot_pl=False, plot_volume=False, plot_drawdown=False, smooth_equity=False, relative_equity=True, 
superimpose=True, resample=False, reverse_indicators=False, open_browser=True)
stat._trades.sort_values(by="EntryBar").head(20)