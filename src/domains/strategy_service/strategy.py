import vectorbt as vbt
import pandas as pd
from src.persistence.yf import read_asset_data
from src.domains.strategy_service.strategies import atr, rsi

def calc_indicators(col, container, indicator, dict_indicators):
    dict_indicators_columns = {"open_", "high", "low", "close", "volume"}
    ticker = "BTC-GBP"
    asset_data = read_asset_data(ticker).data[ticker]
    asset_data = pd.DataFrame.from_dict(asset_data, orient='columns') # orient='index', columns=asset_data_cols)
    asset_data_cols = ['Open','High','Low','Close','Volume','Dividends','Stock Splits']
    # asset_data.columns = asset_data_cols
    # asset_data.columns = set(k.lower() for k in asset_data.columns)
    for i in dict_indicators:                                   # Replace value with data[value]
        if i in dict_indicators_columns:
            col_name = i.title().rstrip("_")
            dict_indicators[i] = asset_data[col_name]
    TA = vbt.IndicatorFactory.from_pandas_ta(indicator)         # pandas-ta indicator
    ta = TA.run(**dict_indicators)
    output_names = ta.output_names
    functions_dict = {
        "rsi": rsi,
        "atrr": atr,
    }
    for name in output_names:
        if name in functions_dict:
            entries, exits, fig = functions_dict[name](ta)
            portfolio = vbt.Portfolio.from_signals(              # Strategy
                asset_data["Close"], entries, exits, init_cash=10000
            )
            fig_portfolio = portfolio.plot()
            tuple_return = (
                col.text(portfolio.stats(silence_warnings=True)),
                container.subheader("Indicator"),
                container.plotly_chart(fig, use_container_width=True),
                container.subheader("Strategy"),
                container.plotly_chart(fig_portfolio, use_container_width=True),
            )
            return tuple_return
        else:
            tuple_return = ()
            tuple_return = tuple_return + (
                container.text(name),
                container.dataframe(getattr(ta, name)),
            )