from Action import Action
import SQLService
import time
import SubscriberService
import string
import Queue
from ActionType import *
from stock import Stock

period = 0;
stockList = {}
cashBase = 0;
TICKERS = []

def runOrder(ticker):
	val = Action(ActionType.ORDERS, ticker).run()
	transTypes = "BID"
	tickers = val["TICKER"]
	bidPrices= val["BID_PRICE"]
	quantitys= val["BID_QUANTITY"]
	#for transType,ticker, price, quantity in zip(transTypes,tickers, bidPrices, quantitys):
		#SQLService.insertOrder(transType, period, ticker, price, quantity)

	transTypes = "ASK"
	tickers = val["TICKER"]
	askPrices= val["ASK_PRICE"]
	quantitys= val["ASK_QUANTITY"]
	#for transType,ticker, price, quantity in zip(transTypes,tickers, askPrices, quantitys):
	#	SQLService.insertOrder(transType, period, ticker, price, quantity)

	return (bidPrices, askPrices)

def batchOrders():
	for name in TICKERS:
		runOrder(name)

def runSecurities():
	global stockList;

	val = Action(ActionType.SECURITIES).run()
	oursecurityDivs = Action(ActionType.MY_SECS).run()
	tickers = val["TICKER"]
	nws= val["NET_WORTH"]
	drs= val["DIV_RATIO"]
	vols= val["VOL"]

	drDict = {};

	for tick, dr in zip(oursecurityDivs["TICKER"], oursecurityDivs["DIV_RATIO"]):
		drDict[tick] = dr;

	for tick, nw, dr, vol in zip(tickers, nws, drs, vols):
		SQLService.insertStock(period, tick, nw, dr, vol)
		if (tick in stockList):
			spread = runOrder(tick)
			if (len(spread[0]) > 0 and len(spread[1]) > 0):
				minVal = min(spread[1])
				maxVal = max(spread[0])
				midMarket = max(spread[0]) + (max(spread[0]) - minVal)/2
				stockList[tick].addTick(midMarket,nw,'',drDict[tick],'',vol,'',spread[0], spread[1]);
				buy = stockList[tick].bidSlopeChange
				if (buy[1] and buy[0] > 0.0005):
					print "BUy" + str(buy)
					price = maxVal
					stockList[tick].buyStock(5,price,1);
				sell = stockList[tick].askSlopeChange
				if (sell[1] and abs(sell[0]) > 0.0005):
					print sell
					price = minVal
					stockList[tick].sellStock(5, price, 1);
					print "Sell " + str(sell) + " on " + str(tick)

def createStocks():
	global stockList;
	vals =  Action(ActionType.SECURITIES).run();
	for key in vals["TICKER"]:
		stockList[key] = Stock(key)

if (__name__ == "__main__"):
	SQLService.connectToDB()
	#SubscriberService.subscribeToUpdates()
	createStocks()
	cashBase = Action(ActionType.MY_CASH).run()[ActionType.MY_CASH]
	while (True):
		if period == 0:
			runSecurities()
			cursor = SQLService.getUniqueTickers()
			batchOrders()
		else:
			runSecurities()
		# 	batchOrders()
		period = period + 1
	SQLService.closeDBConnection()

