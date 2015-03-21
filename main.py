from Action import Action
import SQLService
import time
import SubscriberService
import string
from ActionType import *
from stock import Stock

period = 0;
stockList = {}

TICKERS = []

def runOrder(ticker):
	val = Action(ActionType.ORDERS, ticker).run()
	transTypes = "BID"
	tickers = val["TICKER"]
	bidPrices= val["BID_PRICE"]
	quantitys= val["BID_QUANTITY"]
	for transType,ticker, price, quantity in zip(transTypes,tickers, bidPrices, quantitys):
		SQLService.insertOrder(transType, period, ticker, price, quantity)

	transTypes = "ASK"
	tickers = val["TICKER"]
	askPrices= val["ASK_PRICE"]
	quantitys= val["ASK_QUANTITY"]
	for transType,ticker, price, quantity in zip(transTypes,tickers, askPrices, quantitys):
		SQLService.insertOrder(transType, period, ticker, price, quantity)

	return (bidPrices, askPrices)

def batchOrders():
	for name in TICKERS:
		runOrder(name)

def runSecurities():
	global stockList;

	val = Action(ActionType.SECURITIES).run()
	tickers = val["TICKER"]
	nws= val["NET_WORTH"]
	drs= val["DIV_RATIO"]
	vols= val["VOL"]

	for tick, nw, dr, vol in zip(tickers, nws, drs, vols):
		SQLService.insertStock(period, tick, nw, dr, vol)
		if (tick in stockList):
			spread = runOrder(tick)
			if (len(spread[0]) > 0 and len(spread[1]) > 0):
				minVal = min(spread[1])
				midMarket = max(spread[0]) + (max(spread[0]) - minVal)/2
				stockList[tick].addTick(midMarket,'',dr,'',vol,'',spread[0], spread[1]);
				buy = stockList[tick].bidSlopeChange
				print buy
				if (buy[1] and buy[0] > 0.001):
					price = minVal
					Action(ActionType.BID, tick + " " + str(price) + " 2" ).run()
				#sell = stockList[tick].askSlopeChange
				#print sell

def createStocks():
	global stockList;
	GOOG_TICKER = "GOOG"
	stockList[GOOG_TICKER] = Stock(GOOG_TICKER);
	GOOG_TICKER = "TSLA"
	stockList[GOOG_TICKER] = Stock(GOOG_TICKER);
	GOOG_TICKER = "EA"
	stockList[GOOG_TICKER] = Stock(GOOG_TICKER);
	GOOG_TICKER = "XOM"
	stockList[GOOG_TICKER] = Stock(GOOG_TICKER);
	GOOG_TICKER = "MSFT"
	stockList[GOOG_TICKER] = Stock(GOOG_TICKER);

if (__name__ == "__main__"):
	SQLService.connectToDB()
	#SubscriberService.subscribeToUpdates()
	createStocks()
	while (True):
		if period == 0:
			runSecurities()
			cursor = SQLService.getUniqueTickers()
			for name in cursor.fetchall():
				TICKERS.append(name[0])
			batchOrders()
		else:
			runSecurities()
		# 	batchOrders()
		time.sleep(1)
		period = period + 1
	SQLService.closeDBConnection()

