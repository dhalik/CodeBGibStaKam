import scipy.stats as stats
import scipy.stats as uniform
import numpy as np

##Contracts:
##buyStock(self,amount,price, time); all parameters are numbers
##sellStock(self,amount,price, time); all parameters are numbers
##addTick(self, price, earnings, divRatio, MVPS, vol, div, bid, ask); bid and ask must be lists, rest are numbers
##volBoundOnNormDist(); returns [L,U,isNorm]
##volBoundOnUniDist(); returns [L,U,p,isUni]
##isVolConstant(); returns T/F if volatility is constant
##isVolNormal(); returns T/F if volatility is Normal
##isVolUniform(); returns T/F if volatility is Uniform
##bidSlopeChange; returns (a,b) where a is current bid slope and b is a bool if slope changed

class Stock:
	def __init__(self, ticker):
		self.ticker = ticker
		self.MAPeriod = 7;
		self.outstandingShares=0
		self.shares = 0
		self.initialDiv = 0
		self.volDistribution = ''

		#SlopeChange = (a,b) where a is the current bid slope and b is a bool determining if the slope changed
		self.bidSlopeChange = (0,False)
		self.askSlopeChange = (0,False)
		self.netWorthSlopeChange = (0,False)
		self.bidAvg=[]
		self.askAvg=[]

		self.bidSlope = []
		self.askSlope = []
		self.netWorthSlope = []

		self.PurchaseHistory = []
		self.Earnings = []
		self.DivRatio = []
		self.MVPS = []
		self.Vol = []
		self.Dividends = []
		self.Price = []
		self.NetWorth=[]

	def buyStock(self, amount, price, time):
		self.shares = self.shares+amount
		self.PurchaseHistory.append(['Buy',time,amount,price])

	def sellStock(self, amount, price, time):
		self.shares = self.shares - amount
		self.PurchaseHistory.append(['Sell', time, amount, price])

	def currentValueOfPosition(self, currentMarketPrice):
		return currentMarketPrice * self.shares

	def addBidAskPrice(self, bid, ask):
		if (len(bid) > 0):
			self.bidAvg.append(sum(bid)/len(bid))
		if (len(ask) > 0):
			self.askAvg.append(sum(ask)/len(ask))


	def addBidAskSlope(self):
		if (len(self.bidAvg) >= self.MAPeriod):
			slope = (self.bidAvg[-1] - self.bidAvg[-self.MAPeriod])/self.MAPeriod
			self.bidSlope.append(slope)
		if (len(self.askAvg) >= self.MAPeriod):
			slope = (self.askAvg[-1] - self.askAvg[-self.MAPeriod])/self.MAPeriod
			self.askSlope.append(slope)

	def addNetWorthSlope(self):
		if(len(self.NetWorth) >= 3):
			slope = (self.NetWorth[-1] - self.NetWorth[-3])/3
			self.netWorthSlope.append(slope)

	def updateSlopeTuples(self):
		bidChange = False
		askChange = False
		netWorthSlopeChange = False

		if (len(self.bidSlope) >=2):
			if ((self.bidSlope[-1] > 0 and self.bidSlope[-2] < 0) or (self.bidSlope[-1] < 0 and self.bidSlope[-2] > 0)):
				bidChange = True
			self.bidSlopeChange = (self.bidSlope[-1], bidChange)
		if (len(self.askSlope) >=2):
			if ((self.askSlope[-1] > 0 and self.askSlope[-2] < 0) or (self.askSlope[-1] < 0 and self.askSlope[-2] > 0)):
				askChange = True
			self.askSlopeChange = (self.askSlope[-1], askChange)

		if(len(self.netWorthSlope) >= 2):
			if ((self.netWorthSlope[-1] > 0 and self.netWorthSlope[-2] < 0) or (self.netWorthSlope[-1] < 0 and self.netWorthSlope[-2] > 0)):
				netWorthSlopeChange = True
			self.netWorthSlopeChange = (self.netWorthSlope[-1], netWorthSlopeChange)

	#num:price, earnings, divRatio, MVPS, vol, div
	#list: bid, ask
	def addTick(self, price, networth, earnings, divRatio, MVPS, vol, div, bid, ask):
		if price != '':
			self.Price.append(price)
		if earnings != '':
			self.Earnings.append(earnings)
		if divRatio != '':
			self.DivRatio.append(divRatio)
		if MVPS != '':
			self.MVPS.append(MVPS);
		if vol != '':
			self.Vol.append(vol)
		if div != '':
			self.Dividends.append(div)
		if networth != '':
			self.NetWorth.append(networth)

		if (len(bid) != 0):
			bid.remove(min(bid))
		if (len(ask) !=0):
			ask.remove(max(ask))


		self.addBidAskPrice(bid,ask)
		self.addBidAskSlope()
		self.addNetWorthSlope()

		self.updateSlopeTuples()


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
	AAPL.addTick(0,123123,1,2,3,4,'',[-10,-9,-8],[10,9,8])
	AAPL.addTick(0,999,1,2,3,4,'',[-7,-6,-5],[7,6,5])
	AAPL.addTick(0,4,1,2,3,4,'',[-4,-3,-2],[4,3,2])
	AAPL.addTick(0,45644897,1,2,3,4,'',[-10,-11,-12],[10,11,12])
	#AAPL.addTick(0,1,2,3,4,'',[11,12,13],[1,2,3])
	print AAPL.Earnings
	print AAPL.DivRatio
	print AAPL.MVPS
	print AAPL.Vol
	print AAPL.Dividends
