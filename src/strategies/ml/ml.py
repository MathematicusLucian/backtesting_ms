import numpy as np
import pandas as pd
from backtesting import Backtest
from backtesting.test import EURUSD, SMA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from src.strategies.bollinger import bbands
from src.strategies.ml.ml_utils import get_clean_Xy
from src.strategies.ml.ml_train_once import MLTrainOnceStrategy

def ml():
    data = EURUSD.copy()
    data = bbands(data, SMA)
    X, y = get_clean_Xy(data)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5, random_state=0)
    clf = KNeighborsClassifier(7)  # Model the output based on 7 "nearest" examples
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    _ = pd.DataFrame({'y_true': y_test, 'y_pred': y_pred}).plot(figsize=(15, 2), alpha=.7)
    print('Classification accuracy: ', np.mean(y_test == y_pred))

    bt = Backtest(data, MLTrainOnceStrategy, commission=.0002, margin=.05)
    # bt = Backtest(data, MLWalkForwardStrategy, commission=.0002, margin=.05)
    
    bt.run()
    bt.plot()