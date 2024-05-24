import streamlit as st
import pandas as pd
import pandas_ta as ta
import inspect
from src.core.asset_data_service.asset_data_service import crypto_currencies, fetch_asset_data, trad_currencies
from src.domains.strategy_simulation_service.utils import list_indicators
from src.domains.strategy_simulation_service.strategy_simulation_service import StrategySimService

def fetch_asset_data_for_ticker(ticker):
    asset_data = fetch_asset_data(ticker)
    return pd.DataFrame.from_dict(asset_data, orient='columns') # orient='index', columns=asset_data_cols)
    # asset_data_cols = ['Open','High','Low','Close','Volume','Dividends','Stock Splits']
    # asset_data.columns = asset_data_cols
    # asset_data.columns = set(k.lower() for k in asset_data.columns)

def plot_indicator(indicator, entries, exits):
    fig = indicator.vbt.plot()
    entries.vbt.signals.plot_as_entry_markers(indicator, fig=fig)
    exits.vbt.signals.plot_as_exit_markers(indicator, fig=fig)
    return fig

def run_strategies(strategy_simulation, init_cash, select_asset, select_asset_base, col2, container, select_indicator, list_args):
    ticker = f"{select_asset}-{select_asset_base}"
    asset_data = fetch_asset_data_for_ticker(ticker)
    strategies_outcome = strategy_simulation.run_strategies(
        asset_data, init_cash, select_indicator, list_args
    )
    if not strategies_outcome["entries"].empty:
        col2.text(strategies_outcome["portfolio"].stats(silence_warnings=True))
        container.subheader("Indicator")
        fig = plot_indicator(strategies_outcome["indicator"], strategies_outcome["plot_entries"], strategies_outcome["plot_exits"])
        container.plotly_chart(fig, use_container_width=True)
        container.subheader("Strategy")
        fig_portfolio = strategies_outcome["portfolio"].plot()
        container.plotly_chart(fig_portfolio, use_container_width=True)
    else:
        container.text(strategies_outcome["name"])
        container.dataframe(strategies_outcome["name_attr"])

def indicators_args(indicator_function):
    selected_indicators = inspect.getfullargspec(indicator_function)
    list_args = {}
    for argument in selected_indicators.args:
        name_text_input = f"{argument}input"
        data_set = {"open_", "high", "low", "close", "volume"}
        text_set = {"mamode"} 
        bool_set = {"talib"}
        if argument in text_set:
            name_text_input = st.text_input(argument)
        elif argument in bool_set:
            name_text_input = st.radio(argument, options=(True, False))
        elif argument not in data_set:
            name_text_input = st.number_input(argument, step=1)
        list_args[argument] = name_text_input
    return list_args

def main():
    strategy_simulation = StrategySimService()
    container = st.container()  
    container.header("Backtesting App"),
    col1, col2 = st.columns([4, 4])
    container.write("")
    with col1:
        select_asset = st.selectbox("Convert from", crypto_currencies)
        select_asset_base = st.selectbox("To base", trad_currencies)
        select_indicator = st.selectbox("Pandas-ta indicator", ["rsi", "atr"])      # indicators = list_indicators()  
        indicator_function = getattr(ta, select_indicator)
        selected_indicators = indicators_args(indicator_function)
        st.button("Run Simulation", on_click=run_strategies, args=(strategy_simulation, 10000, select_asset, select_asset_base, col2, container, select_indicator, selected_indicators))
        st.sidebar.write(indicator_function.__doc__)