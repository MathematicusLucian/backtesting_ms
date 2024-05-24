# backtesting-ms

fetches asset data - pandas

calculate indicators

    TA = vbt.IndicatorFactory.from_pandas_ta(indicator)  
    TA.run(**dict_indicators)

loop over strategies

    run stategy

    vbt.Portfolio.from_signals(
        asset data close, 
        asset data entries, 
        asset data exit, 
        cash)
--------
fetches asset data

in/out samples (rolling)

simulate holding -> sharpe ratio

in-sharpe (simulate all params)
    best_index (in-sharpe)
        performance[performance.groupby('split_idx').idxmax()].index
    best_params -> fast, and slow: vbt.MA.run
        entries = fast_ma.ma_above(slow_ma) #, crossover=True)
        exits = fast_ma.ma_below(slow_ma) #, crossover=True)
        pf = vbt.Portfolio.from_signals
        sharpe_ratio

out-sharpe (simulate all params)
    best_index (out-sharpe)

## DynamicBT: A wrapper for Backtesting.py

This wrapper is an enhancement of the Python library ``backtesting.py``, which is very popular for backtesting of trading strategies.

***Will extract this as a seperate repo, and deploy to PyPi as a library***

Issues addressed:
- ``backtesting.py`` relies on hardcoding of strategy configuration, such as upper and lower bands, and also the optimisation criteria, etc., meaning much code has to be written to define strategies.
- The default strategies, and many circulated online, are not going to find alpha (an opportunity to exploit market inefficiency); because they are utilised by too many traders. 

Solution:
- The wrapper assembles strategy details according to content of either a config file, or a database. (WIP: This can then be edited via a UI.)
- There is a factory to fetch the strategy class.
- Walkforward testing of all strategies.
- Strategies, with optimisation functionality, are required that compare data sources of world events, including news events and social media sentiment, to market movements to find patterns that reflect correlation. [market_sentiment_ms](https://github.com/MathematicusLucian/market_sentiment_ms)
- Optimsiation can be ehanced with machine learning [stonk-value-forecasting-model](https://github.com/MathematicusLucian/stonk-value-forecasting-model)

## Backtesting some popular technical indicators
| Image | Details |
|---|---|
| ![Strats](./assets/strats.png) | **``strategies`` folder:** Typical technical indicators, such as Average Direction Movemement, Bollinger Bands, Donchian, EMA, MAC, MACD, Mean Reversion, Momentum, RSI, SMA, Stochastic, etc., and combinations of these. |

### Bollinger Bands
![Bollinger chart](./assets/bollinger.png)

### SMA (Simple Moving Average)
![SMA chart](./assets/sma.png)

**Sample stategy**
- 10-day SMA below 30-day SMA.
- 10-day and 30-day SMA above 50-day SMA.
- 10-day, 30-day, and 50-day SMA below 200-day SMA.

### MACD (Moving Average Convergence/Divergence)
Purpose: Entry/exit points; trend confirmation; and risk management.

![MACD chart](./assets/macd.png)

The MACD indicator is derived from two exponential moving averages (EMAs) — the 12-day EMA and the 26-day EMA. The formula for MACD is as follows:

``MACDLine=12−dayEMA−26−dayEMA``

A signal line, often a 9-day EMA, is plotted on top of the MACD line. This signal line serves as a trigger for buy or sell signals.

``SignalLine=9−dayEMA``

The MACD histogram, the visual representation of the difference between the MACD line and the signal line, provides insights into the strength and direction of the trend.

``MACDHistogram=MACDLine−SignalLine``

2 conditions:
- MACD above the MACD signal.
- MACD greater than 0.