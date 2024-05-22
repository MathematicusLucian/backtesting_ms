def plot_indicator(indicator, entries, exits):
    fig = indicator.vbt.plot()
    entries.vbt.signals.plot_as_entry_markers(indicator, fig=fig)
    exits.vbt.signals.plot_as_exit_markers(indicator, fig=fig)
    return fig