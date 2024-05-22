from src.domains.strategy_service.utils import plot_indicator

def atr(ta):                            # We don't want to trigger buy and sell as atr is just a metric
    entries = ta.atrr_below(20)
    exits = ta.atrr_below(20)
    indicator = ta.rsi
    return {
        "indicator": indicator, 
        "entries": entries, 
        "exits": exits,
        "plot_entries": entries, 
        "plot_exits": exits
    }