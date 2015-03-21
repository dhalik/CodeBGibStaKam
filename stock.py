import scipy.stats as stats
import scipy.stats as uniform
import numpy as np

class Stock:    
	def __init__(self, ticker):
		self.ticker = ticker
		self.outstandingShares=0
		self.shares = 0
		self.initialDiv = 0
		self.volDistribution = ''

		self.bidAvg=[]
		self.askAvg=[]        
		self.PurchaseHistory = []
		self.Earnings = []
		self.DivRatio = []
		self.MVPS = []
		self.Vol = []
		self.Dividends = []
		self.Price = []
		self.bidAvg=[]
		self.askAvg=[]
		
	def buyStock(self, amount, price, time):
		self.shares = self.shares+amount
		self.PurchaseHistory.append(['Buy',time,amount,price])
		
	def sellStock(self, amount, price, time):
		self.shares = self.shares - amount
		self.PurchaseHistory.append(['Sell', time, amount, price])
		
	def currentValueOfPosition(self, currentMarketPrice):
		return currentMarketPrice * self.shares


	#num:price, earnings, divRatio, MVPS, vol, div
	#list: bid, ask
	def addTick(self, price, earnings, divRatio, MVPS, vol, div):
		if price != '': 
			self.Price.append(price);
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

			
	#Assuming we have div calculated
	def calcEarnings(self, div, divRatio):
		earnings = (div*self.outstandingShares)/divRatio
		return earnings

	def calcNextEarning(self, volatility, currentEarnings):
		try:
			earnings = currentEarnings/(1+volatility)
			return earnings
		except ZeroDivisionError:
			print "Zero Division: failed to calculate Next earnings"
			
	
	def calcTotalShares(self):
		pass

	#===========================Volatility calculations================ 
	def isVolNormal(self):
		pVal = 0
		if (len(self.Vol)> 8):
			pVal = stats.normaltest(self.Vol)[1]
		if (pVal > 0.05):
			return True
		else:
			return False
	def isVolUniform(self):
		pVal = stats.kstest(self.Vol,'uniform', args=(min(self.Vol),max(self.Vol)))[1]

		if (pVal > 0.05):
			return True
		else:
			return False
	def isVolConstant(self):
		return all(self.Vol[0] == item for item in self.Vol)
		
	def stdOfVolatility(self):
		return np.std(self.Vol)
	
	def meanOfVolatility(self):
		return np.mean(self.Vol)

	#Normal Distribution Bound: using the current STD, function returns lowerbound, upperbound, isNormal
	def volBoundOnNormDist(self):
		mean = self.meanOfVolatility()
		std = self.stdOfVolatility()
		return [mean - std, mean + std, self.isVolNormal()]

	#Uniform Distribution Bound: returns lowest value, highest value found, probability, isUniform
	def volBoundOnUniDist(self):
		return [min(self.Vol), max(self.Vol), 1/len(self.Vol), self.isVolUniform()]


						  
if __name__ == "__main__":
	AAPL = Stock('AAPL');
	AAPL.addTick(0,1,2,3,4,'')
	print AAPL.Earnings
	print AAPL.DivRatio
	print AAPL.MVPS
	print AAPL.Vol
	print AAPL.Dividends



	
