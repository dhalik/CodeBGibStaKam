from Action import Action
import SQLService
import time
import SubscriberService
from ActionType import *

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

def runOrder(ticker):
 	val = Action(ActionType.ORDERS, ticker).run()
	transType = "BID"
	tickers = val["TICKER"]
	price= val["BID_PRICE"]
	quantity= val["BID_QUANTITY"]
    for transType,tickers, price, quantity in zip(transType,tickers, price, quantity):
        SQLService.insertOrder(transType, period, tickers, price, quantity) 
 	
 	transType = "ASK"
    tickers = val["TICKER"]
    price= val["ASK_PRICE"]
    quantity= val["ASK_QUANTITY"]
    for transType,tickers, price, quantity in zip(transType,tickers, price, quantity):
        SQLService.insertOrder(transType, period, tickers, price, quantity) 
	
def runSecurities():
	val = Action(ActionType.SECURITIES).run()
	    tickers = val["TICKER"]
	    nws= val["NET_WORTH"]
	    drs= val["DIV_RATIO"]
	    vols= val["VOL"]
	    for tick, nw, dr, vol in zip(tickers, nws, drs, vols):
	        SQLService.insertStock(period, tick, nw, dr, vol)

if (__name__ == "__main__"):
	SQLService.connectToDB()
	while (True):
		runSecurities()
		runOrder(GOOG_TICKER)
		runOrder(AAPL_TICKER)
		runOrder(ATVI_TICKER)
		runOrder(EA_TICKER)
		runOrder(FB_TICKER)
		runOrder(MSFT_TICKER)
		runOrder(SNY_TICKER)
		runOrder(TSLA_TICKER)
		runOrder(TWTR_TICKER)
		runOrder(XOM_TICKER)
	    time.sleep(1)
	    period = period + 1

