from src.domains.strategy_service.utils import plot_indicator

def rsi(ta):                                                    # Indicator functions
    entries = ta.rsi_crossed_above(70)
    exits = ta.rsi_crossed_below(30)
    clean_entries, clean_exits = entries.vbt.signals.clean(exits)
    fig = plot_indicator(ta.rsi, clean_entries, clean_exits)
    return entries, exits, fig