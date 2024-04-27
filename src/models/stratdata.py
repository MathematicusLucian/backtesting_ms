import pandas as pd
from pydantic import BaseModel
from backtesting import Backtest, Strategy

class StratData(BaseModel):
    pd.DataFrame
    Backtest
    int