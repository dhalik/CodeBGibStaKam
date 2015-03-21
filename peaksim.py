from Action import Action
import SQLService
import time
import SubscriberService
import string
from ActionType import *
#import stock

period = 0;
AAPL_TICKER = 'AAPL'
ATVI_TICKER = 'ATVI'
EA_TICKER = 'EA'
FB_TICKER = 'FB'
GOOG_TICKER = 'GOOG'
MSFT_TICKER = 'MSFT'
SNY_TICKER = 'SNY'
TSLA_TICKER = 'TSLA'
TWTR_TICKER = 'TWTR'
XOM_TICKER = 'XOM'
stockList = {}

TICKERS = []

def runOrder(ticker):
	val = Action(ActionType.ORDERS, ticker).run()
	transType = "BID"
	tickers = val["TICKER"]
	price= val["BID_PRICE"]
	quantity= val["BID_QUANTITY"]
	for transType,tickers, price, quantity in zip(transType,tickers, price, quantity):
		SQLService.insertOrder(transType, period, tickers, price, quantity)

	#bestBid = max(price)

	transType = "ASK"
	tickers = val["TICKER"]
	price= val["ASK_PRICE"]
	quantity= val["ASK_QUANTITY"]
	for transType,tickers, price, quantity in zip(transType,tickers, price, quantity):
		SQLService.insertOrder(transType, period, tickers, price, quantity)

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
			spread = getBidAsk()
			midMarket = spread[0] + (spread[0] - spread[1])/2
			print "Midmarket is " + str(midMarket)
			stockList.addTick('',midMarket,dr,'',vol, '');

def createStocks():
	global stockList;
	stockList[GOOG_TICKER] = Stock(GOOG_TICKER);
	stockList[EA_TICKER] = Stock(EA_TICKER);

if (__name__ == "__main__"):
	SQLService.connectToDB()
	while (True):
		if period == 0:
			runSecurities()
			cursor = SQLService.getUniqueTickers()
			for name in cursor.fetchall():
				TICKERS.append(name[0])
			print(TICKERS)
			batchOrders()
		else:
			if period >= 30:
				SQLService.closeDBConnection()
				break
			runSecurities()
			batchOrders()

			if period >= 2:
				for ticker in TICKERS:
					period2 = period -2
					period1 = period - 1
					cursor = SQLService.query("SELECT networth FROM " + SQLService.stocksTableName 
						+ " WHERE ticker = " + name 
						+ " AND period >=" + period2 + " AND period <= " + period1 
						+ " ORDER BY period DESC")
					for name in cursor.fetchall():
						print("NetWorth"+(name[0]))

		period = period + 1
		time.sleep(1)


