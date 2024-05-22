def atr(ta):                         # Don't trigger buy and sell because atr is a metric
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