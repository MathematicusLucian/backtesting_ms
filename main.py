from datetime import datetime, date
# from altair import Stream
from backtesting import Backtest, Strategy
from backtesting.test import GOOG
# from backtesting.lib import crossover, plot_heatmaps, resample_apply
import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
# import matplotlib.pyplot as plt
# import seaborn as sns
from src.services.strategy_service import TradingStrategy_ConcreteCreator

trading_strategies = [
    "AverageDirectionalMovement",
    "BBandRSI",
    # "BBandRSI_WithStopLoss",
    # "BBandRSI_WithShortPosition",
    "BBsigma",
    # "BBsigma_WithShortPosition",
    "DonchianBreakout",
    # "DonchianBreakout_WithShortPosition",
    # "DonchianBreakout_WithATRStopLoss",
    # "DonchianBreakout_WithPercentageStopLoss",
    "EMA_Cross",
    # "EMA_Cross2",
    # "Ema_Cross__WithShortPosition",
    # "EntryRSIandExitSMA_WithShortPosition",
    # "EntryRSI50andExitBB",
    # "EntryRSI50andExitBB_WithShortPosition",
    # "EntryRSI50andExitBBWithATRStopLoss",
    # "GridStrat",
    # "Macd_25",
    # "Macd_25_2"
    # "MACDCross_WithShortPosition",
    # "MACDCross",
    # "MACDStrategy",
    # "MACDandBBD",
    # "MACDandBBD_WithShortPosition",
    # "MACDandRSI",
    # "MACDandRSI_WithShortPosition",
    "MeanReversion",
    "MeanReversionBollinger",
    "Momentum",
    "Momentum__Volatility",
    "MovingAverageCrossover",
    # "RsiOscillator",
    "RsiOscillator__Simple",
    "RsiOscillator__Simple_Close",
    # "RsiOscillator__Single",
    # "RsiOscillator__DailyWeekly",
    "RsiOscillator__LS_Close",
    "SmaCross", 
    "SmaCross__Trailing",
    "Sma4Cross",
    "SMAandRSI",
    "SMAandRSI_WithShortPosition",
    "Stochastic_OverboughtOversold",
    "StopLoss_ATR",
    # "StopLossFix",
    # "StopLoss_Percentage"
    # "StopLoss_Trailing",
    # "System",
    # "Turtle",
    # "Volatility_Breakout"
]

strategy_results_colums = (
    "_strategy",
    "Start",
    "End",
    "Duration",
    "Exposure Time [%]",
    "Equity Final [$]",
    "Equity Peak [$]",
    "Return [%]",
    "Buy & Hold Return [%]",
    "Return (Ann.) [%]",
    "Volatility (Ann.) [%]",
    "Sharpe Ratio",
    "Sortino Ratio",
    "Calmar Ratio",
    "Max. Drawdown [%]",
    "Avg. Drawdown [%]",
    "Max. Drawdown Duration",
    "Avg. Drawdown Duration",
    "Win Rate [%]",
    "Best Trade [%]",
    "Worst Trade [%]",
    "Avg. Trade [%]",
    "Max. Trade Duration",
    "Avg. Trade Duration",
    "Profit Factor",
    "Expectancy [%]"
)

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

def append_row(df, row):
    return pd.concat([
                df, 
                pd.DataFrame([row], columns=row.index)]
           ).reset_index(drop=True)

def determine_optimized_strategy_config(bt):
    return bt.optimize(n1=range(5, 30, 5),
        n2=range(10, 70, 5),
        maximize="Win Rate [%]", #"Equity Final [$]", #"Profit Factor"
        constraint=lambda param: param.n1 < param.n2)

def get_strategy_with_max_result(maximize):
    trading_strategy_factory = TradingStrategy_ConcreteCreator()
    maximum_result=0
    for strat in trading_strategies:
        trading_strategy: type[Strategy] = trading_strategy_factory.get_trading_stategy(strat)
        bt = Backtest(bitcoin_df, trading_strategy, cash=10_000, commission=.002)
        stats = bt.run() # kwargs: set parameters
        if float(stats[maximize]) > float(maximum_result):
            maximum_result = float(stats[maximize])
        # stats = determine_optimized_strategy_config(bt)
        return stats, bt

if __name__ == "__main__":
    asset="BTC-GBP"
    start=date(2014,1,1) 
    end=date.today()
    bitcoin_df:pd.DataFrame = pdr.get_data_yahoo(asset, start=start, end=end) 
    bitcoin_df["Date"] = pd.to_datetime(bitcoin_df.index) 
    maximize="Win Rate [%]"

    stats, bt = get_strategy_with_max_result(maximize)

    strategy_with_maximum_result = stats["_strategy"]
    strategy_results_df = pd.DataFrame(columns=strategy_results_colums)
    strategy_results_df = append_row(strategy_results_df, stats).reindex(columns=strategy_results_colums)
    strategy_results_df.to_csv('strategy_results_df.csv', sep=',', index=False, encoding='utf-8')
    equity_curve = stats["_equity_curve"]
    equity_curve.to_csv('strategy_results_df__equity_curve.csv', sep=',', index=False, encoding='utf-8')
    trades = stats["_trades"]
    trades.to_csv('strategy_results_df__trades', sep=',', index=False, encoding='utf-8')

    # bt.plot(plot_volume=False, plot_pl=False)