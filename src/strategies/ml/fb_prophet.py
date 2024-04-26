# https://facebook.github.io/prophet/docs/quick_start.html
from matplotlib import pyplot as plt
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import date
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

data = pd.df = pdr.DataReader("TSLA","yahoo") #pd.read_csv("stock_data")
n_years = 1
period = n_years*365
data.reset_index(inplace = True)
df_train = data[['Date','Close']]
df_train = df_train.rename(columns = {"Date":"ds", "Close":'y'})

prophet = Prophet(daily_seasonality=True)

future = prophet.make_future_dataframe(periods = period)
forecast = prophet.predict(future)
future_dates = prophet.make_future_dataframe(periods=365)
predictions = prophet.predict(future_dates)
fig = plot_plotly(prophet, predictions)

unknown_data = data.iloc[-90:]
data = data.iloc[:-90]
future_dates(prophet.make_future_dataframe(periods=365))
predictions = prophet.predict(future_dates)
fig = plot_plotly(prophet, predictions)

plt.figure(figsize=(12,8))
pred = predictions[predictions['ds'].isin(unknown_data['ds'])]
plt.plot(pd.to_datetime(unknown_data['ds']), unknown_data['y'], label="Actual")
plt.plot(pd.to_datetime(unknown_data['ds']), pred['yhat'], label="Actual")
plt.legend()

fig = plot_plotly(prophet,forecast)
# fig = prophet.plot(forecast)
fig.savefig('prophet_plot.svg')

fig = prophet.plot_components(forecast)
fig.savefig('prophet_components_plot.svg')