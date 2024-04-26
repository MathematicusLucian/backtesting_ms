from backtesting import Strategy
from src.strategies.bollinger import BBANDS_2

class BBsigma(Strategy):
    n = 25 
    nu = 2 
    nd = 2 

    def init(self):
        self.upper, self.lower = self.I(BBANDS_2, self.data.Close, self.n, self.nu, self.nd)

    def next(self): 
        if self.data.Close > self.upper or self.data.Open > self.upper:
            self.position.close()
        elif self.data.Close < self.lower or self.data.Open < self.lower:
            if not self.position:
                self.buy() 
        # if self.data.Close[-1] > self.upper[-1] :
        #     self.position.close()
        # elif self.data.Close[-1]  < self.lower[-1] :
        #     self.buy() 

class BBsigma_WithShortPosition(Strategy):
    n = 25 
    nu = 2 
    nd = 2

    def init(self):
        self.upper, self.lower = self.I(BB, self.data.Close, self.n, self.nu, self.nd)

    def next(self): 
        if self.data.Close > self.upper or self.data.Open > self.upper:
            if not self.position:
                self.sell()
            else:
                self.position.close()
        elif self.data.Close < self.lower or self.data.Open < self.lower:
            if not self.position:
                self.buy() 