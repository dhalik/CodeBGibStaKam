from ActionType import ActionType
import math
import time
import clientpy2

class Action:

    def __init__(self, action, params=""):
        self._action = action
        self._params = params
        if params != "":
            self._command = action + " " + params
        else:
            self._command = action

    def parse(self, retVal):
        tokens = retVal.split(" ");
        e = {}
        if (tokens[0] == "MY_CASH_OUT"):
            e[ActionType.MY_CASH] = float(tokens[1])
        elif (tokens[0] == "MY_SECURITIES_OUT"):
            e["TICKER"] = []
            e["PRICE"] = []
            e["DIV_RATIO"] = []
            for i in range(0,int(len(tokens)/3)):
                e["TICKER"].append(tokens[i * 3+1])
                e["PRICE"].append(float(tokens[i * 3 + 2]))
                e["DIV_RATIO"].append(float(tokens[i * 3 + 3]))
        elif (tokens[0] == "MY_ORDERS_OUT"):
            e["BID_QUANTITY"] = []
            e["ASK_QUANTITY"] = []
            e["BID_PRICE"] = []
            e["ASK_PRICE"] = []
            if (len(tokens) > 1):
                e["TICKER"] = [tokens[2]]
            for i in range(0,int(len(tokens)/4)):
                if (tokens[i * 4 + 1] == "BID"):
                    e["BID_PRICE"].append(float(tokens[i * 4 + 3]))
                    e["BID_QUANTITY"].append(float(tokens[i * 4 + 4]))
                else:
                    e["ASK_PRICE"].append(float(tokens[i * 4 + 3]))
                    e["ASK_QUANTITY"].append(float(tokens[i*4 + 4]))
        elif (tokens[0] == "SECURITIES_OUT"):
            e["TICKER"] = []
            e["NET_WORTH"] = []
            e["DIV_RATIO"] = []
            e["VOL"] = []
            for i in range(0,int(len(tokens)/4)):
                e["TICKER"].append(tokens[i * 4+1])
                e["NET_WORTH"].append(float(tokens[i * 4 + 2]))
                e["DIV_RATIO"].append(float(tokens[i * 4 + 3]))
                e["VOL"].append(float(tokens[i * 4 + 4]))
        elif (tokens[0] == "SECURITY_ORDERS_OUT"):
            e["BID_QUANTITY"] = []
            e["ASK_QUANTITY"] = []
            e["BID_PRICE"] = []
            e["ASK_PRICE"] = []
            e["TICKER"] = [tokens[2]]
            for i in range(0,int(len(tokens)/4)):
                if (tokens[i * 4 + 1] == "BID"):
                    e["BID_PRICE"].append(float(tokens[i * 4 + 3]))
                    e["BID_QUANTITY"].append(float(tokens[i * 4 + 4]))
                else:
                    e["ASK_PRICE"].append(float(tokens[i * 4 + 3]))
                    e["ASK_QUANTITY"].append(float(tokens[i*4 + 4]))
        elif (tokens[0] == "BID_OUT"):
            print "LOG: BID PLACED: " + self._command
        elif (tokens[0] == "ASK_OUT"):
            print "LOG: ASK PLACED: " + self._command
        elif (tokens[0] == "CLEAR_BID_OUT"):
            print "LOG: BID CLEARED: " + self._command
        elif (tokens[0] == "CLEAR_ASK_OUT"):
            print "LOG: ASK CLEARED: " + self._command
        elif (tokens[0] == "ERROR"):
            print "LOG: ERROR: " + retVal
            raise ValueError("Error raised");
        else:
            print "Unhandled Type: " + retVal
        return e

    def checkParams(self):
        if ((self._action == ActionType.MY_CASH
                or self._action == ActionType.MY_SECS
                or self._action == ActionType.MY_ORDERS
                or self._action == ActionType.SECURITIES)
                and len(self._params) != 0):
            raise ValueError("Too many args")
        elif ((self._action == ActionType.ORDERS
                or self._action == ActionType.CLEAR_BID
                or self._action == ActionType.CLEAR_ASK)
                and len(self._params.split(" ")) != 1):
            raise ValueError("Too many args")
        elif ((self._action == ActionType.BID
                or self._action == ActionType.ASK)
                and len(self._params.split(" ")) != 3):
            raise ValueError("Too many args")

    def run(self):
        self.checkParams()
        print "LOG: executing " + self._command
        self._got = clientpy2.run("Good_Biddies", "asdfghjkl", self._command)
        print "LOG: returned " + self._got
        return self.parse(self._got)

    def __repr__(self):
        return str([self._action, self._params])

if __name__ == "__main__":
    while (True):
        print  Action(ActionType.SECURITIES).run()
        time.sleep(1)
