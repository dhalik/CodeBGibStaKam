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
	prices= val["BID_PRICE"]
	quantitys= val["BID_QUANTITY"]
	for transType,ticker, price, quantity in zip(transTypes,tickers, prices, quantitys):
		SQLService.insertOrder(transType, period, ticker, price, quantity)

	bestBid = max(prices)

	transTypes = "ASK"
	tickers = val["TICKER"]
	prices= val["ASK_PRICE"]
	quantitys= val["ASK_QUANTITY"]
	for transType,ticker, price, quantity in zip(transTypes,tickers, prices, quantitys):
		SQLService.insertOrder(transType, period, ticker, price, quantity)

	bestAsk = max(prices)
	return (bestBid, bestAsk)

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
			midMarket = spread[0] + (spread[0] - spread[1])/2
			print "Midmarket is " + str(midMarket)
			stockList[tick].addTick('',midMarket,dr,'',vol, '');

def createStocks():
	global stockList;
	GOOG_TICKER = "GOOG"
	stockList[GOOG_TICKER] = Stock(GOOG_TICKER);

if (__name__ == "__main__"):
	SQLService.connectToDB()
	createStocks()
	while (True):
		if period == 0:
			runSecurities()
			cursor = SQLService.getUniqueTickers()
			for name in cursor.fetchall():
				TICKERS.append(name[0])
			print(TICKERS)
			batchOrders()
		else:
			SQLService.closeDBConnection()
			break
		# 	runSecurities()
		# 	batchOrders()
		time.sleep(1)
		period = period + 1


