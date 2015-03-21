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
    time.sleep(1)
    period = period + 1
