import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from itertools import cycle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

projection_Monero = 5
projection_Ethereum = 5
projection_Bitcoin = 5

# --------------
# --- Monero ---
# --------------
Monero = pdr.DataReader("MON-USD","yahoo")
Monero['Prediction'] = Monero[['Close']].shift(-projection_Monero)
visualize_Monero = cycle(['Open','Close','High','Low','Prediction'])
fig = px.line(Monero, x=Monero.Date, y=[Monero['Open'], Monero['Close'], 
                                          Monero['High'], Monero['Low'], Monero['Prediction']],
             labels={'Date': 'Date','value':'Price'})
fig.update_layout(title_text='Monero', font_size=15, font_color='black',legend_title_text='Parameters')
fig.for_each_trace(lambda t:  t.update(name = next(visualize_Monero)))
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
fig.show()
X_Monero = np.array(Monero[['Close']])
X_Monero = X_Monero[:-projection_Monero]
y_Monero = Monero['Prediction'].values
y_Monero = y_Monero[:-projection_Monero]
x_train_Monero, x_test_Monero, y_train_Monero, y_test_Monero = train_test_split(X_Monero,y_Monero,test_size=0.15)
linReg_Monero = LinearRegression()
linReg_Monero.fit(x_train_Monero,y_train_Monero)
linReg_confidence_Monero = linReg_Monero.score(x_test_Monero,y_test_Monero)
print("Linear Regression Confidence for Monero: ",linReg_confidence_Monero)
print(linReg_confidence_Monero*100,'%')
x_projection_Monero = np.array(Monero[['Close']])[-projection_Monero:]
linReg_prediction_Monero = linReg_Monero.predict(x_projection_Monero)

# ----------------
# --- Ethereum ---
# ----------------
Ethereum = pdr.DataReader("ETH-USD","yahoo")
Ethereum['Prediction'] = Ethereum[['Close']].shift(-projection_Ethereum)
visualize_Ethereum = cycle(['Open','Close','High','Low','Prediction'])
fig = px.line(Ethereum, x=Ethereum.Date, y=[Ethereum['Open'], Ethereum['Close'], 
                                          Ethereum['High'], Ethereum['Low'],Ethereum['Prediction']],
             labels={'Date': 'Date','value':'Price'})
fig.update_layout(title_text='Ethereum', font_size=15, font_color='black',legend_title_text='Parameters')
fig.for_each_trace(lambda t:  t.update(name = next(visualize_Ethereum)))
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
fig.show()
X_Ethereum = np.array(Ethereum[['Close']])
X_Ethereum = X_Ethereum[:-projection_Ethereum]
y_Ethereum = Ethereum['Prediction'].values
y_Ethereum = y_Ethereum[:-projection_Ethereum]
x_train_Ethereum, x_test_Ethereum, y_train_Ethereum, y_test_Ethereum = train_test_split(X_Ethereum,y_Ethereum,test_size=0.15)
linReg_Ethereum = LinearRegression()
linReg_Ethereum.fit(x_train_Ethereum,y_train_Ethereum)
linReg_confidence_Ethereum = linReg_Ethereum.score(x_test_Ethereum,y_test_Ethereum)
print("Linear Regression Confidence for Ethereum: ",linReg_confidence_Ethereum)
print(linReg_confidence_Ethereum*100,'%')
x_projection_Ethereum = np.array(Ethereum[['Close']])[-projection_Ethereum:]
linReg_prediction_Ethereum = linReg_Ethereum.predict(x_projection_Ethereum)

# ---------------
# --- Bitcoin ---
# ---------------
Bitcoin = pdr.DataReader("BTC-USD","yahoo")
Bitcoin['Prediction'] = Bitcoin[['Close']].shift(-projection_Bitcoin)
visualize_Bitcoin = cycle(['Open','Close','High','Low','Prediction'])
fig = px.line(Bitcoin, x=Bitcoin.Date, y=[Bitcoin['Open'], Bitcoin['Close'], 
                                          Bitcoin['High'], Bitcoin['Low'],Bitcoin['Prediction']],
             labels={'Date': 'Date','value':'Price'})
fig.update_layout(title_text='Bitcoin', font_size=15, font_color='black',legend_title_text='Parameters')
fig.for_each_trace(lambda t:  t.update(name = next(visualize_Bitcoin)))
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
fig.show()
X_Bitcoin = np.array(Bitcoin[['Close']])
X_Bitcoin = X_Bitcoin[:-projection_Bitcoin]
y_Bitcoin = Bitcoin['Prediction'].values
y_Bitcoin = y_Bitcoin[:-projection_Bitcoin]
x_train_Bitcoin, x_test_Bitcoin, y_train_Bitcoin, y_test_Bitcoin = train_test_split(X_Bitcoin,y_Bitcoin,test_size=0.15)
linReg_Bitcoin = LinearRegression()
linReg_Bitcoin.fit(x_train_Bitcoin,y_train_Bitcoin)
linReg_confidence_Bitcoin = linReg_Bitcoin.score(x_test_Bitcoin,y_test_Bitcoin)
print("Linear Regression Confidence for Bitcoin: ",linReg_confidence_Bitcoin)
print(linReg_confidence_Bitcoin*100,'%')
x_projection_Bitcoin = np.array(Bitcoin[['Close']])[-projection_Bitcoin:]
linReg_prediction_Bitcoin = linReg_Bitcoin.predict(x_projection_Bitcoin)
