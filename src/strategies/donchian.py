from backtesting import Strategy
import pandas as pd
import talib as ta
import numpy as np

def CalcDonchian_High(values, donchian_span_long):
    donchianline = pd.Series(values)
    return donchianline.rolling(window = donchian_span_long).max()

def CalcDonchian_Low(values, donchian_span_short):
    donchianline = pd.Series(values)
    return donchianline.rolling(window = donchian_span_short).min()

def CalcATR(phigh, plow, pclose, period):
    high = pd.Series(phigh)
    low = pd.Series(plow)
    close = pd.Series(pclose)
    return ta.ATR(\
        np.array(high).astype("double"),\
        np.array(low).astype("double"),\
        np.array(close).astype("double"),\
        timeperiod=period)

class DonchianBreakout(Strategy):
    donchian_long = 20
    donchian_short = 10
    atr_period = 20

    def init(self):
        self.donchian_high = self.I(CalcDonchian_High, self.data.High, self.donchian_long)
        self.donchian_low = self.I(CalcDonchian_Low, self.data.Low, self.donchian_short)
        self.atr = self.I(CalcATR, self.data.High,  self.data.Low, self.data.Close, self.atr_period)

    def next(self): 
        price = self.data.Close[-1]
        if price > self.donchian_high[-2]:
            if not self.position:
                self.buy() 
        elif price < self.donchian_low[-2]:
            self.position.close()

# class DonchianBreakout_WithSMACrossover(Strategy):

class DonchianBreakout_WithShortPosition(Strategy):
    donchian_long = 20
    donchian_short = 10
    atr_period = 20

    def init(self):
        self.donchian_high = self.I(CalcDonchian_High, self.data.High, self.donchian_long) 
        self.donchian_low = self.I(CalcDonchian_Low, self.data.Low, self.donchian_short)
        self.atr = self.I(CalcATR, self.data.High,  self.data.Low, self.data.Close, self.atr_period)

    def next(self): 
        price = self.data.Close[-1]
        if price > self.donchian_high[-2]:
            if not self.position:
                self.buy() 
        elif price < self.donchian_low[-2]:
            if not self.position:
                self.sell()
            else:
                self.position.close()

class DonchianBreakout_WithATRStopLoss(Strategy):
    donchian_long = 40
    donchian_short = 20
    atr_period = 20
    atr_entrytime = 0

    def init(self):
        self.donchian_high = self.I(CalcDonchian_High, self.data.High, self.donchian_long)
        self.donchian_low = self.I(CalcDonchian_Low, self.data.Low, self.donchian_short)
        self.atr = self.I(CalcATR, self.data.High,  self.data.Low, self.data.Close, self.atr_period)

    def next(self): 
        price = self.data.Close[-1]
        atr_entrytime = self.atr[-1]

        if self.position and self.trades[-1].size > 0 and self.trades[-1].entry_price < price - atr_entrytime * 2:
            self.position.close()
        elif self.position and self.trades[-1].size < 0 and self.trades[-1].entry_price > price + atr_entrytime * 2:
            self.position.close()
        elif price > self.donchian_high[-2]:
            if not self.position:
                self.buy() 
        elif price < self.donchian_low[-2]:
            self.position.close() 

class DonchianBreakout_WithPercentageStopLoss(Strategy):
    donchian_long = 20
    donchian_short = 10
    atr_period = 20

    def init(self):
        self.donchian_high = self.I(CalcDonchian_High, self.data.High, self.donchian_long)
        self.donchian_low = self.I(CalcDonchian_Low, self.data.Low, self.donchian_short)
        self.atr = self.I(CalcATR, self.data.High,  self.data.Low, self.data.Close, self.atr_period)

    def next(self):
        price = self.data.Close[-1]
        if self.position and self.position.pl_pct < -0.075:
            self.position.close() 
        elif price > self.donchian_high[-2]:
            if not self.position:
                self.buy() 
        elif price < self.donchian_low[-2]:
            self.position.close()