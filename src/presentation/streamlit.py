import streamlit as st
import plotly.figure_factory as ff
import pandas as pd
import pandas_ta as ta
import inspect
import vectorbt as vbt
from src.core.asset_data_service.asset_data_service import crypto_currencies, fetch_asset_data, fetch_asset_data__close, trad_currencies
from src.domains.backtesting_service.w_fwd.walkforward_o import Walkforward_Optimisation
from src.domains.strategy_simulation_service.utils import list_indicators
from src.domains.strategy_simulation_service.strategy_simulation_service import StrategySimService

color_schema = vbt.settings['plotting']['color_schema']
color1 = color_schema['blue']
color2 = color_schema['orange']

st.set_page_config
st.markdown("""
    <style>
    section, .element-container {
        float: left !important;
    }
    p, input, div {
        font-size: 0.7rem !important;
    }
    pre code {
        font-size: 0.6rem !important;
    }
    div, input {
        margin: 2px 1.5px !important;
        padding: 0px !important;
    }
    button {
        padding: 5px !important;
    }       
    section {
        align-items: start !important;
    }
    section > div {
        margin: 0 !important;
        padding: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

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

def run_strategies(select_simulation_type, init_cash, select_asset, select_asset_base, input_number_of_days, container, select_indicator, list_args):
    ticker = f"{select_asset}-{select_asset_base}"
    if(select_simulation_type == "Run Strategy"):
        strategy_simulator = StrategySimService(input_number_of_days)
        asset_data = fetch_asset_data_for_ticker(ticker)
        strategies_outcome = strategy_simulator.run_strategies(
            asset_data, init_cash, select_indicator, list_args
        )
        if not strategies_outcome["entries"].empty:
            container.text(strategies_outcome["portfolio"].stats(silence_warnings=True))
            container.subheader("Indicator")
            fig = plot_indicator(strategies_outcome["indicator"], strategies_outcome["plot_entries"], strategies_outcome["plot_exits"])
            container.plotly_chart(fig, use_container_width=True)
            container.subheader("Strategy")
            fig_portfolio = strategies_outcome["portfolio"].plot()
            container.plotly_chart(fig_portfolio, use_container_width=True)
        else:
            container.text(strategies_outcome["name"])
            container.dataframe(strategies_outcome["name_attr"])
    else:
        asset_data = fetch_asset_data__close(ticker)   
        strategy = 'MA'
        wfo = Walkforward_Optimisation(strategy, asset_data, input_number_of_days)
        wfo.in_sample_simulation()
        wfo.out_sample_simulation()
        group_labels = ['in_sample_hold', 'in_sample_median', 'in_sample_best', 'out_sample_hold', 'out_sample_median', 'out_sample_test']
        strategies_outcome = wfo.optimisation_results()
        hist_data = [strategies_outcome['in_sample_hold'],
            strategies_outcome['in_sample_median'],
            strategies_outcome['in_sample_best'],
            strategies_outcome['out_sample_hold'],
            strategies_outcome['out_sample_median'],
            strategies_outcome['out_sample_test']]
        # fig = vbt.plot(trace_kwargs=[
        #         dict(line_color=color1), dict(line_color=color1, line_dash='dash'), dict(line_color=color1, line_dash='dot'),
        #         dict(line_color=color2), dict(line_color=color2, line_dash='dash'), dict(line_color=color2, line_dash='dot')])
        fig = ff.create_distplot(hist_data, group_labels) #, bin_size=[.1, .25, .5])
        container.plotly_chart(fig, use_container_width=True)
        container.dataframe(wfo.optimisation_results__df())

def indicators_args(sidebar_col2, indicator_function):
    selected_indicators = inspect.getfullargspec(indicator_function)
    list_args = {}
    for argument in selected_indicators.args:
        name_text_input = f"{argument}input"
        data_set = {"open_", "high", "low", "close", "volume"}
        text_set = {"mamode"} 
        bool_set = {"talib"}
        if argument in bool_set:
            name_text_input = sidebar_col2.radio(argument, options=(True, False))
        elif argument in text_set:
            name_text_input = sidebar_col2.text_input(argument)
        elif argument not in data_set:
            name_text_input = sidebar_col2.number_input(argument, step=1)
        list_args[argument] = name_text_input
    return list_args

def main():
    container = st.container()  
    with st.sidebar:
        st.header("Backtesting App"),
        select_simulation_type = st.radio("Simulation type", options=("Walkforward Optimisation", "Run Strategy"))
        sidebar_col1, sidebar_col2 = st.columns([2, 2])
        select_asset = sidebar_col1.selectbox("Convert from", options=crypto_currencies())
        select_asset_base = sidebar_col1.selectbox("To base", options=trad_currencies())
        input_number_of_days = sidebar_col1.number_input("Number of days", step=1)
        select_strategy = sidebar_col1.selectbox("Strategy (pandas-ta)", ["rsi", "atr"])      # indicators = list_indicators()  
        strategy_function = getattr(ta, select_strategy)
        strategy_args = indicators_args(sidebar_col2, strategy_function)
        st.button("Run Simulation", on_click=run_strategies, args=(select_simulation_type, 10000, select_asset, select_asset_base, input_number_of_days, container, select_strategy, strategy_args))
        strategy_description = strategy_function.__doc__
        st.markdown(strategy_description, unsafe_allow_html=True)