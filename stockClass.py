class Stock:    
    def __init__(self, ticker):
        self.ticker = ticker
        self.outstandingShares=0;
        self.shares = 0
        self.initialDiv = 0
        
        self.PurchaseHistory = []
        self.Earnings = []
        self.DivRatio = []
        self.MVPS = []
        self.Vol = []
        self.Dividends = []

    def buyStock(self, amount, price, time):
        self.shares = self.shares+amount
        self.PurchaseHistory.append(['Buy',time,amount,price])
        
    def sellStock(self, amount, price, time):
        self.shares = self.shares - amount
        self.PurchaseHistory.append(['Sell', time, amount, price])
        
    def currentValueOfPosition(self, currentMarketPrice):
        return currentMarketPrice * self.shares
        
    def addTick(self, earnings, divRatio, MVPS, vol, div):
        if earnings != '':
            self.Earnings.append(earnings);
        if divRatio != '':     
            self.DivRatio.append(divRatio);
        if MVPS != '': 
            self.MVPS.append(MVPS);
        if vol != '': 
            self.Vol.append(vol);
        if div != '': 
            self.Dividends.append(div);
            
    def calculateVolDist(self, volatility):
        pass
    
    def calcEarnings(self, div, divRatio):
        earnings = (div*self.outstandingShares)/divRatio
        return earnings

    def calcNextEarning(self, volatility, currentEarnings):
        earnings = currentEarnings/(1+volatility)
        return earnings
    
    def calcTotalShares(self):
        pass

    
if __name__ == "__main__":
    AAPL = Stock('AAPL');
    AAPL.addTick(1,2,3,4,'')
    print AAPL.Earnings
    print AAPL.DivRatio
    print AAPL.MVPS
    print AAPL.Vol
    print AAPL.Dividends
    
    
