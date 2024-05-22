import vectorbt as vbt

btc_price = vbt.YFData.download("BTC-USD")
closing_prices = btc_price.get("Close")
rsi = vbt.RSI.run(closing_prices)       # strategy
entries = rsi.rsi_crossed_below(30)
exits = rsi.rsi_crossed_above(70)

print(entries)

portfolio = vbt.Portfolio.from_signals(closing_prices, entries, exits, init_cash=10000)
portfolio.plot().show()