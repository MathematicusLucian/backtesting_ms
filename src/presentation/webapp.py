import streamlit as st
import pandas_ta as ta
import inspect
from src.domains.strategy_service.pandas_ta_utils import list_indicators
from src.domains.strategy_service.strategy import calc_indicators

def main():
    container = st.container()  
    container.header("Backtesting App"),
    col1, col2 = st.columns([4, 4])
    container.write("")
    with col1:
        indicators = list_indicators()  
        # select_indicator = st.selectbox("Pandas-ta indicator", indicators)
        select_indicator = st.selectbox("Pandas-ta indicator", ["rsi", "atr"])
        indicator_function = getattr(ta, select_indicator)
        arguments = inspect.getfullargspec(indicator_function)
        list_args = {}
        for argument in arguments.args:
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
        st.button("Run", on_click=calc_indicators, args=(col2, container, select_indicator, list_args))
        st.sidebar.write(indicator_function.__doc__)