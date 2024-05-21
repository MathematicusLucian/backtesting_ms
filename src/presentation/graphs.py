# pf.plot_positions().show()
pf.plot_drawdowns().show()
pf.plot(subplots = ['drawdowns','trades']).show()
fig = pf.plot(subplots = [ 
    ('RSI', dict(
        title = 'RSI',
        yaxis_kwargs=dict(title='RSI'),
        check_is_not_grouped=True,
        ))
    ],
    make_subplots_kwargs = dict(rows=5,cols=1,shared_xaxes='all')
)
scatter_rsi = vbt.plotting.Scatter(
    data = rsi.rsi,
    x_labels = rsi.rsi.index,
    trace_names = ["RSI"],
    add_trace_kwargs=dict(row=2, col=1),
    fig=fig
)
fig.show()
fig = pf.plot(subplots = [ 
    'orders',
    ('RSI', dict(
        title = 'RSI',
        yaxis_kwargs=dict(title='RSI'),
        check_is_not_grouped=True,
        ))
    ],
    make_subplots_kwargs = dict(rows=5,cols=1,shared_xaxes='all')
)
scatter_rsi = vbt.plotting.Scatter(
        data = rsi.rsi,
        x_labels = rsi.rsi.index,
        trace_names = ["RSI"],
        add_trace_kwargs=dict(row=2, col=1),
        fig=fig
            )
fig.show()
fig = fig.add_hline(  y=70,
                line_color="#858480",
                row = 2,
                col = 1,
                line_width = 5
)
fig = fig.add_hline(  y=30,
                line_color="#858480",
                row = 2,
                col = 1,
                line_width = 5
)
fig.show()