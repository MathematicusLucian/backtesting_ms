

    rsi = vbt.RSI.run(asset_data, window=21)
    entries = rsi.rsi_crossed_above(60)
    exits = rsi.rsi_crossed_below(30)
    pf = vbt.Portfolio.from_signals(asset_data, entries, exits)
    # # print(pf)
    # # pf.plot().show()

    split_kwargs = dict(  # 30 windows, each 2 years long, reserve 180 days for test
        n=30, 
        window_len=365 * 2, 
        set_lens=(180,), 
        left_to_right=False
    )
    pf_kwargs = dict(direction='both', freq='d')    # long and short
    windows = np.arange(10, 50)

    # roll_in_and_out_samples(price, **split_kwargs, plot=True, trace_names=['in-sample', 'out-sample']).show()
    (in_price, in_indexes), (out_price, out_indexes) =roll_in_and_out_samples(asset_data, **split_kwargs)
    # print(in_price.shape, len(in_indexes))  # in-sample
    # print(out_price.shape, len(out_indexes))  # out-sample
    in_hold_sharpe = simulate_holding(in_price, **pf_kwargs)
    # print(in_hold_sharpe)
    in_best_index = get_best_index(in_hold_sharpe)
    # print(in_best_index)
    # in_best_fast_windows = get_best_params(in_best_index, 'fast_window')
    # in_best_slow_windows = get_best_params(in_best_index, 'slow_window')
    # in_best_window_pairs = np.array(list(zip(in_best_fast_windows, in_best_slow_windows)))
    # print(in_best_window_pairs)
    # pd.DataFrame(in_best_window_pairs, columns=['fast_window', 'slow_window']).vbt.plot().show()
    # out_hold_sharpe = simulate_holding(out_price, **pf_kwargs)
    # print(out_hold_sharpe)
    # out_sharpe = simulate_all_params(out_price, windows, **pf_kwargs)   # Simulate all params for out-sample ranges
    # print(out_sharpe)
    # out_test_sharpe = simulate_best_params(out_price, in_best_fast_windows, in_best_slow_windows, **pf_kwargs)  # Use best params from in-sample ranges and simulate them for out-sample ranges
    # print(out_test_sharpe)
    # cv_results_df = pd.DataFrame({
    #     'in_sample_hold': in_hold_sharpe.values,
    #     'in_sample_median': in_sharpe.groupby('split_idx').median().values,
    #     'in_sample_best': in_sharpe[in_best_index].values,
    #     'out_sample_hold': out_hold_sharpe.values,
    #     'out_sample_median': out_sharpe.groupby('split_idx').median().values,
    #     'out_sample_test': out_test_sharpe.values
    # })
    # color_schema = vbt.settings['plotting']['color_schema']
    # cv_results_df.vbt.plot(
    #     trace_kwargs=[
    #         dict(line_color=color_schema['blue']),
    #         dict(line_color=color_schema['blue'], line_dash='dash'),
    #         dict(line_color=color_schema['blue'], line_dash='dot'),
    #         dict(line_color=color_schema['orange']),
    #         dict(line_color=color_schema['orange'], line_dash='dash'),
    #         dict(line_color=color_schema['orange'], line_dash='dot')
    #     ]
    # ).show()