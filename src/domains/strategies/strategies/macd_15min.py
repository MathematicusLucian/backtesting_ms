from backtesting import Strategy
from backtesting import Backtest
from datetime import datetime
import pandas as pd
import pandas_ta as ta
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tqdm import tqdm
tqdm.pandas()

def ema_signal(df, current_candle, backcandles):
    df_slice = df.reset_index().copy()
    start = max(0, current_candle - backcandles)
    end = current_candle
    relevant_rows = df_slice.iloc[start:end]
    if all(relevant_rows['High'] < relevant_rows['EMA']):
        return 1
    elif all(relevant_rows['Low'] > relevant_rows['EMA']):
        return 2
    else:
        return 0

def total_signal(df, current_candle, backcandles):
    if (ema_signal(df, current_candle, backcandles)==2 and
        all(df.loc[current_candle - 3:current_candle - 2, "MACD"] < df.loc[current_candle - 3:current_candle - 2, "MACD_signal"]) and
        all(df.loc[current_candle - 1:current_candle, "MACD"] > df.loc[current_candle - 1:current_candle, "MACD_signal"])
        ):
            return 2
    if (ema_signal(df, current_candle, backcandles)==1 and
        all(df.loc[current_candle - 3:current_candle - 2, "MACD"] > df.loc[current_candle - 3:current_candle - 2, "MACD_signal"]) and
        all(df.loc[current_candle - 1:current_candle, "MACD"] < df.loc[current_candle - 1:current_candle, "MACD_signal"])
        ):

            return 1
    return 0

def pointpos(x):
    if x['TotalSignal']==2:
        return x['Low']-1e-3
    elif x['TotalSignal']==1:
        return x['High']+1e-3
    else:
        return np.nan

def SIGNAL():
    return dfopt.TotalSignal

class Macd_25(Strategy):
    size = 3000
    slcoef = 1.1
    TPSLRatio = 1.5
    #rsi_length = 16
    
    def init(self):
        super().init()
        self.signal1 = self.I(SIGNAL)
        #df['RSI']=ta.rsi(df.Close, length=self.rsi_length)

    def next(self):
        super().next()
        slatr = self.slcoef*self.data.ATR[-1]
        TPSLRatio = self.TPSLRatio
        # if len(self.trades)>0:
        #     if self.trades[-1].is_long and self.data.rsi[-1]>=90:
        #         self.trades[-1].close()
        #     elif self.trades[-1].is_short and self.data.rsi[-1]<=10:
        #         self.trades[-1].close()
        if self.signal1==2 and len(self.trades)==0:
            sl1 = self.data.Close[-1] - slatr
            tp1 = self.data.Close[-1] + slatr*TPSLRatio
            self.buy(sl=sl1, tp=tp1, size=self.size)
        elif self.signal1==1 and len(self.trades)==0:         
            sl1 = self.data.Close[-1] + slatr
            tp1 = self.data.Close[-1] - slatr*TPSLRatio
            self.sell(sl=sl1, tp=tp1, size=self.size)

class Macd_25_2(Strategy):
    size = 3000
    slcoef = 2.3
    TPSLRatio = 1.6
    #rsi_length = 16
    
    def init(self):
        super().init()
        self.signal1 = self.I(SIGNAL)
        #df['RSI']=ta.rsi(df.Close, length=self.rsi_length)

    def next(self):
        super().next()
        slatr = self.slcoef*self.data.ATR[-1]
        TPSLRatio = self.TPSLRatio

        # if len(self.trades)>0:
        #     if self.trades[-1].is_long and self.data.rsi[-1]>=90:
        #         self.trades[-1].close()
        #     elif self.trades[-1].is_short and self.data.rsi[-1]<=10:
        #         self.trades[-1].close()
        
        if self.signal1==2 and len(self.trades)==0:
            sl1 = self.data.Close[-1] - slatr
            tp1 = self.data.Close[-1] + slatr*TPSLRatio
            self.buy(sl=sl1, tp=tp1, size=self.size)
        
        elif self.signal1==1 and len(self.trades)==0:         
            sl1 = self.data.Close[-1] + slatr
            tp1 = self.data.Close[-1] - slatr*TPSLRatio
            self.sell(sl=sl1, tp=tp1, size=self.size)

# bt = Backtest(dfopt, Strat, cash=250, margin=1/30, commission=0.00) # type: ignore
# stats, heatmap = bt.optimize(slcoef=[i/10 for i in range(10, 26)],
#                     TPSLRatio=[i/10 for i in range(10, 26)],
#                     #rsi_length=[5, 8, 10, 12, 14, 16], 
#                     maximize='Return [%]', max_tries=300,
#                         random_state=0,
#                         return_heatmap=True)
# df = pd.read_csv("EURUSD_Candlestick_15_M_BID_01.02.2023-17.02.2024.csv")
# df["Gmt time"]=df["Gmt time"].str.replace(".000","")
# df['Gmt time']=pd.to_datetime(df['Gmt time'],format='%d.%m.%Y %H:%M:%S')
# df=df[df.High!=df.Low]
# df.set_index("Gmt time", inplace=True, drop=True)
# df["EMA"]=ta.ema(df.Close, length=200)
# macd = ta.macd(df.Close)
# df['MACD'], df['MACD_signal'], df['MACD_hist'] = macd.iloc[:,0], macd.iloc[:,1], macd.iloc[:,2]
# df['ATR']=ta.atr(df.High, df.Low, df.Close, length=7)
# df.describe()
# df=df[-20000:-1]
# df.reset_index(inplace=True)
# df['EMASignal'] = df.progress_apply(lambda row: ema_signal(df, row.name, 5) if row.name >= 20 else 0, axis=1)
# df['TotalSignal'] = df.progress_apply(lambda row: total_signal(df, row.name, 7) if row.name != 0 else 0, axis=1)
# df[df.TotalSignal != 0].head(20)
# df['pointpos'] = df.apply(lambda row: pointpos(row), axis=1)
# st=1100
# dfpl = df[st:st+350]
# #dfpl.reset_index(inplace=True)
# fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
#                 open=dfpl['Open'],
#                 high=dfpl['High'],
#                 low=dfpl['Low'],
#                 close=dfpl['Close'])])
# fig.add_scatter(x=dfpl.index, y=dfpl['pointpos'], mode="markers",
#                 marker=dict(size=5, color="MediumPurple"),
#                 name="entry")
# fig.show()

# dfopt = df[:]
# stats["_strategy"]
# heatmap_df = heatmap.unstack()
# plt.figure(figsize=(10, 8))
# sns.heatmap(heatmap_df, annot=True, cmap='viridis', fmt='.0f')
# plt.show()

# bt = Backtest(dfopt, Strat2, cash=250, margin=1/30, commission=0.00)
# stats = bt.run()
# bt.plot()