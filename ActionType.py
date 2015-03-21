from enum import Enum

class ActionType(Enum):
    MY_CASH = "MY_CASH"
    MY_SECS = "MY_SECURITIES"
    MY_ORDERS = "MY_ORDERS"
    SECURITIES = "SECURITIES"
    ORDERS = "ORDERS"
    BID = "BID"
    ASK = "ASK"
    CLEAR_BID = "CLEAR_BID"
    CLEAR_ASK = "CLEAR_ASK"

if __name__ == "__main__":
    print ActionType.MY_CASH
#to add the rest...
