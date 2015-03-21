from Action import Action
import SQLService
import time
import SubscriberService
from ActionType import *

SQLService.connectToDB()
period = 0;
while (True):
    val = Action(ActionType.SECURITIES).run()
    tickers = val["TICKER"]
    nws= val["NET_WORTH"]
    drs= val["DIV_RATIO"]
    vols= val["VOL"]
    for tick, nw, dr, vol in zip(tickers, nws, drs, vols):
        SQLService.insertStock(period, tick, nw, dr, vol)

    val = Action(ActionType.ORDERS).run()
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
    
    time.sleep(1)
    period = period + 1

