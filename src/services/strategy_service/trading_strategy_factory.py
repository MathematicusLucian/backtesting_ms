import warnings
warnings.filterwarnings("ignore")
from datetime import datetime, date
from abc import ABC, abstractmethod
# from altair import Stream
from backtesting import Backtest, Strategy
from backtesting.test import GOOG
# from backtesting.lib import crossover, plot_heatmaps, resample_apply
import yfinance as yf
from pandas_datareader import data as pdr
# import matplotlib.pyplot as plt
# import seaborn as sns
from src.models.stratdata import StratData
from src.strategies import *

class TradingStrategyCreator(ABC):
    @abstractmethod
    def get_trading_stategy(self):
        return "blah"

class TradingStrategy_ConcreteCreator(TradingStrategyCreator):
    def get_trading_stategy(self, targetclass):
        # params={}
        # params["n1"]=1
        # params["n2"]=200
        return globals()[targetclass]

def optim_func(series):
    if series["Expectancy [%]"] < 0:
        return -1
    if series["Max. Drawdown [%]"] > 20:
        return -1
    if series["Profit Factor"] < 1:
        return -1
    if series["Sharpe Ratio"] < 1.5:
        return -1
    if series["SQN"] < 2.5:
        return -1
    if series["# Trades"] < 7:
        return -1
    if series["Win Rate [%]"] < 40:
        return -1
    if series["Worst Trade [%]"] < -20:
        return -1
    return series["Equity Final [$]"]

# ml() #SciKit Machine Learning

def get_asset_data(asset, start, end) -> pd.DataFrame:
    asset_df:pd.DataFrame = pdr.get_data_yahoo(asset, start=start, end=end) 
    asset_df["Date"] = pd.to_datetime(asset_df.index) 
    return asset_df

def append_row(df, row):
    return pd.concat([
            df, 
            pd.DataFrame([row], columns=row.index)
        ]).reset_index(drop=True)

def save_to_csv(df, file_name):
    df.to_csv(f'./results/{file_name}.csv', sep=',', index=False, encoding='utf-8')

def get_constraint(strat):
    if strat in ["SmaCross","SmaCross__Trailing","Sma4Cross"]:
        return lambda param: param.n1 < param.n2
    elif strat in ["RsiOscillator__DailyWeekly", "RsiOscillator__Single", "StopLossFix", "StopLoss_Percentage", "StopLoss_Trailing"]:
        return None 
    else:
        return None
    # AverageDirectionalMovement adx_period adx_threshold
    # BBandRSI BBandRSI_WithShortPosition EntryRSI50andExitBB EntryRSI50andExitBB_WithShortPosition n = 25 nu = 2 nd = 2 upper_bound = 70 lower_bound = 30 rsi_window = 14
    # EntryRSI50andExitBBWithATRStopLoss n = 25 nu = 2 nd = 2 upper_bound = 50 lower_bound = 50 rsi_window = 14 atr_period = 20
    # BBandRSI_WithStopLoss n = 25 nu = 2 nd = 2 upper_bound = 70 lower_bound = 30 rsi_window = 14 stop_loss_perc = -7.5
    # BBsigma BBsigma_WithShortPosition n = 25 nu = 2 nd = 2
    # DonchianBreakout DonchianBreakout_WithShortPosition DonchianBreakout_WithPercentageStopLoss donchian_long = 20 donchian_short = 10 atr_period = 20
    # DonchianBreakout_WithATRStopLoss donchian_long = 20 donchian_short = 10 atr_period = 20 atr_entrytime
    # EMA_Cross EMA_Cross2 Ema_Cross__WithShortPosition EMA_short = 10 EMA_long = 20
    # GridStrat size
    # MovingAverageCrossover short_period long_period
    # Macd_25 Macd_25_2 size = 3000 slcoef = 1.1 TPSLRatio = 1.5
    # MACDandBBD MACDandBBD_WithShortPosition MACD_short = 12 MACD_long = 26 MACD_signal = 9 MACD_threshold = 0 bollinger_period = 25 bollinger_upper_sigma = 2 bollinger_lower_sigma = 2
    # MACDandRSI MACDandRSI_WithShortPosition MACDshort = 12 MACDlong = 26 MACDsignal = 9 MACDThreshold = 0 upper_bound = 70 lower_bound = 30 rsi_window = 14
    # MACDStrategy params = (('fast', 12), ('slow', 26), ('signal', 9)) 
    # MACDCross MACDCross_WithShortPosition MACD_short = 12 MACD_long = 26 MACD_signal = 9 MACD_threshold_plus = 0 MACD_threshold_minus = -150
    # MeanReversionBollinger lookback_period = 40 z_score_threshold = 3
    # MeanReversion lookback_period = 21 z_score_threshold = 3.0
    # Momentum small_threshold = 0 large_threshold = 3 period_long = 7 period_short = 2
    # Momentum__Volatility lookback_period = 10 atr_period = 15 atr_threshold = 2.5
    # RsiOscillator__Simple RsiOscillator__Simple_Close ww_rsi = 14 oversold_level = 30 overbought_level = 70
    # RsiOscillator upper_bound=60lower_bound=40rsi_window=12atr_window=14atr_stoploss=4atr_takeprofit=8
    # RsiOscillator__Single RsiOscillator__DailyWeekly None
    # RsiOscillator__LS_Close s_rsi = 6 l_rsi = 24 ww_rsi = 14 oversold_level = 20 overbought_level = 80
    # "SMAandRSI","SMAandRSI_WithShortPosition", EntryRSIandExitSMA_WithShortPosition SMA_short = 10 SMA_long = 30 upper_bound = 70 lower_bound = 30 rsi_window = 14 
    # "Stochastic_OverboughtOversold" stoch_period = 14 stoch_threshold_oversold = 45 stoch_threshold_overbought = 80
    # "StopLoss_ATR" n = 14
    # StopLossFix StopLoss_Percentage StopLoss_Trailing None
    # System d_rsi = 30 w_rsi = 30 level = 70
    # Turtle entry_lookback = 10 exit_lookback = 20
    # Volatility_Breakout lookback_period = 20 volatility_factor = 1.5 stop_loss_percentage = 0.02 take_profit_percentage = 0.02

def determine_optimized_strategy_indicator_values(strat_name, bt):
    c = get_constraint(strat_name)
    if c == None:
        return strat_name
    return bt.optimize(n1=range(5, 30, 5),
        n2=range(10, 70, 5),
        maximize="Win Rate [%]", #"Equity Final [$]", #"Profit Factor"
        constraint=c)

def load_strat(strat) -> type[Strategy]:
    trading_strategy_factory = TradingStrategy_ConcreteCreator()
    return trading_strategy_factory.get_trading_stategy(strat)

def get_strategy_with_max_result(asset:pd.DataFrame, trading_strategies, maximisation_metric:str) -> StratData:
    strongest_strategy_stats:pd.DataFrame=None
    strongest_bt:Backtest=None
    strongest_maximize_result:int=0
    for strat_name in trading_strategies:
        trading_strategy = load_strat(strat_name)
        bt = Backtest(asset, trading_strategy, cash=10_000, commission=.002)
        stats = bt.run() # kwargs: set parameters
        c = determine_optimized_strategy_indicator_values(strat_name, bt)
        print(c)
        # stats = stats if c == None else c
        # print(stats)
        if float(stats[maximisation_metric]) > float(strongest_maximize_result):
            strongest_maximize_result = float(stats[maximisation_metric])
            strongest_bt = bt
            strongest_strategy_stats = stats
    return strongest_strategy_stats, strongest_bt, strongest_maximize_result