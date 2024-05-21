from backtesting import Backtest
# https://kernc.github.io/backtesting.py/doc/examples/Parameter%20Heatmap%20&%20Optimization.html
import matplotlib.pyplot as plt
import seaborn as sns

def optim_func(series):
    if series['# Trades'] < 10:
        return -1
    else:
        return series['Equity Final [$]']/series['Exposure Time [%]']

def create_heatmap(bt: Backtest):
    output, heatmap = bt.optimize(
        upper_bound = range(50,85,5),
        lower_bound = range(15,45,5),
        rsi_window = range(10,30,2),
        # maximize='Equity Final [$]'
        maximize=optim_func,
        return_heatmap=True
    )
    hm = heatmap.groupby(["upper_bound","lower_bound"]).mean().unstack()
    sns.heatmap(hm, cmap="plasma")
    plt.show()

# Heatmap
# backtest = Backtest(GOOG, Sma4Cross, commission=.002)
# stats, heatmap = backtest.optimize(
#     n1=range(10, 110, 10),
#     n2=range(20, 210, 20),
#     n_enter=range(15, 35, 5),
#     n_exit=range(10, 25, 5),
#     constraint=lambda p: p.n_exit < p.n_enter < p.n1 < p.n2,
#     maximize='Equity Final [$]',
#     max_tries=200,
#     random_state=0,
#     return_heatmap=True)
# heatmap.sort_values().iloc[-3:]
# hm = heatmap.groupby(['n1', 'n2']).mean().unstack()
# sns.heatmap(hm[::-1], cmap='viridis')
# plot_heatmaps(heatmap, agg='mean')
# stats_skopt, heatmap, optimize_result = backtest.optimize(
#     n1=[10, 100],      # Note: For method="skopt", we
#     n2=[20, 200],      # only need interval end-points
#     n_enter=[10, 40],
#     n_exit=[10, 30],
#     constraint=lambda p: p.n_exit < p.n_enter < p.n1 < p.n2,
#     maximize='Equity Final [$]',
#     method='skopt',
#     max_tries=200,
#     random_state=0,
#     return_heatmap=True,
#     return_optimization=True)
# heatmap.sort_values().iloc[-3:]
# from skopt.plots import plot_objective, plot_evaluations
# _ = plot_objective(optimize_result, n_points=10)
# _ = plot_evaluations(optimize_result, bins=10)