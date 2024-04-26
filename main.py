from datetime import datetime, date
from pydantic import BaseModel
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

class StratData(BaseModel):
    int
    Backtest
    pd.DataFrame

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

def save_to_csv(df, file_name):
    df.to_csv(f'./results/{file_name}.csv', sep=',', index=False, encoding='utf-8')

def determine_optimized_strategy_config(bt):
    return bt.optimize(n1=range(5, 30, 5),
        n2=range(10, 70, 5),
        maximize="Win Rate [%]", #"Equity Final [$]", #"Profit Factor"
        constraint=lambda param: param.n1 < param.n2)

def load_strat(strat) -> type[Strategy]:
    trading_strategy_factory = TradingStrategy_ConcreteCreator()
    return trading_strategy_factory.get_trading_stategy(strat)

def get_strategy_with_max_result(asset:pd.DataFrame, maximisation_metric:str) -> StratData:
    strongest_maximize_result:int=0
    strongest_bt:Backtest=None
    strongest_stats:pd.DataFrame=None
    for strat in trading_strategies:
        trading_strategy = load_strat(strat)
        bt = Backtest(asset, trading_strategy, cash=10_000, commission=.002)
        stats = bt.run() # kwargs: set parameters
        # stats = determine_optimized_strategy_config(bt)
        if float(stats[maximisation_metric]) > float(strongest_maximize_result):
            strongest_maximize_result = float(stats[maximisation_metric])
            strongest_bt = bt
            strongest_stats = stats
    return strongest_stats, strongest_bt, strongest_maximize_result

def get_asset_data(asset, start, end):
    asset_df:pd.DataFrame = pdr.get_data_yahoo(asset, start=start, end=end) 
    asset_df["Date"] = pd.to_datetime(asset_df.index) 
    return asset_df

if __name__ == "__main__":
    asset_df = get_asset_data("BTC-GBP", date(2014,1,1), date.today())
    maximize_metric_name="Win Rate [%]"
    
    # Backtest to calculate strongest strat
    strongest_strat, strongest_bt, strongest_maximize_result = get_strategy_with_max_result(asset_df, maximize_metric_name)
    print(strongest_strat["_strategy"], strongest_maximize_result)

    # Save results to CSV files
    strongest_strat_df = append_row(pd.DataFrame(columns=strategy_results_colums), strongest_strat) \
        .reindex(columns=strategy_results_colums)
    list(map(save_to_csv, 
        (strongest_strat_df, strongest_strat["_equity_curve"], strongest_strat["_trades"]), 
        ("strongest_strat", "strongest_strat__equity_curve", "strongest_strat__trades"))
    )
    # Plot chart
    strongest_bt.plot(plot_volume=False, plot_pl=False)