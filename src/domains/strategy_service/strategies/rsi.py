from src.domains.strategy_service.utils import plot_indicator

def rsi(ta):                                   # Indicator functions
    entries = ta.rsi_crossed_above(70)
    exits = ta.rsi_crossed_below(30)
    clean_entries, clean_exits = entries.vbt.signals.clean(exits)
    indicator = ta.rsi
    return {
        "indicator": indicator, 
        "entries": entries, 
        "exits": exits,
        "plot_entries": clean_entries, 
        "plot_exits": clean_exits
    }