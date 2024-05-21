import vectorbt as vbt

def simulate_all_params_MACD(price, fast_windows, slow_windows, signal_windows, **kwargs):
    # Run MACD indicator
    macd_ind = vbt.MACD.run(price, fast_window=fast_windows, slow_window=slow_windows, signal_window=signal_windows)
    
    # Entry when MACD is above zero AND signal
    entries = macd_ind.macd_above(0) & macd_ind.macd_above(macd_ind.signal) 

    # Exit when MACD is below zero OR signal
    exits = macd_ind.macd_below(0) | macd_ind.macd_below(macd_ind.signal)

    # Build portfolio 
    pf = vbt.Portfolio.from_signals(price, entries, exits,**kwargs)

    # Draw all window combinations as a 3D volume
    fig = pf.sharpe_ratio().vbt.volume(
        x_level='macd_fast_window',
        y_level='macd_slow_window',
        z_level='macd_signal_window',
        slider_level='split_idx',
        trace_kwargs=dict(
            colorbar=dict(
                title='Sharpe Ratio', 
            )
        )
    )
    fig.show()

    return pf