def get_constraint(strat):
    if strat in ["SmaCross","SmaCross__Trailing","Sma4Cross"]:
        return lambda param: param.n1 < param.n2
    elif strat in ["RsiOscillator"]:
        return lambda param: param.upper_bound > param.lower_bound
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