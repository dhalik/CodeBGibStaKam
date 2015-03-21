#SQL DB
import sqlite3
import string

dbName = 'gibstankam.db'
stocksTableName = 'stocks'
transactionsTableName = 'transactions'
ordersTableName = 'orders'
conn = None

def connectToDB():	
	global conn
	conn = sqlite3.connect(dbName)
	conn.text_factory = str
	
	c = conn.cursor()
	# Create table
	#c.execute("DROP TABLE if exists " + stocksTableName + "")
	#c.execute("DROP TABLE if exists " + transactionsTableName + "")
	c.execute("CREATE TABLE IF NOT EXISTS " + stocksTableName + "(period integer, ticker text, networth double, dividendratio double, volatility double)")
	c.execute("CREATE TABLE IF NOT EXISTS " + transactionsTableName + "(type text, period integer, ticker text, price double, shares integer)")
	c.execute("CREATE TABLE IF NOT EXISTS " + ordersTableName + "(type text, period integer, ticker text,  price double, shares integer)")
	# Save (commit) the changes
	conn.commit()
	

def getStockInfoForTicker(ticker):
	t = (ticker,)
	c = conn.cursor()
	c.execute("SELECT * FROM " + stocksTableName+ " WHERE ticker=?", t)
	return c

#Only use this if you are really friggin lazy...
def getStockInfoForQuery(query):
	c = conn.cursor()
	c.execute(query)
	return c

def getAllStocks():
	c = conn.cursor()
	c.execute("SELECT * FROM " + stocksTableName)
	return c

def insertStock(period,ticker,networth,dividendratio,volatility):
	global conn
	c = conn.cursor()
	c.execute("INSERT INTO " + stocksTableName
		+ " VALUES ('" + str(period) + "','" + ticker +"','"+ str(networth) + "','"+str(dividendratio)+ "','"+ str(volatility) + "')")
	conn.commit()

def getAllTransactions():
	c = conn.cursor()
	c.execute("SELECT * FROM " + transactionsTableName)
	return c


def insertTransaction(transType, period, ticker, price, shares):
	global conn
	c = conn.cursor()
	c.execute("INSERT INTO " + transactionsTableName
		+ " VALUES ('" + str(transType) + "','" + str(period) + "','" + str(ticker) + "','" + str(price) +"','"+ str(shares) + "')")
	conn.commit()

def insertOrder(transType, period, ticker, price, shares):
	global conn
	c = conn.cursor()
	c.execute("INSERT INTO " + ordersTableName
		+ " VALUES ('" + str(transType) + "','" + str(period) + "','" + str(ticker) + "','" + str(price) +"','"+ str(shares) + "')")
	conn.commit()

def getOrdersForQuery(query):
	c = conn.cursor()
	c.execute(query)
	return c

def closeDBConnection():
	global conn
	conn.close()

def getUniqueTickers():
	c = conn.cursor()
	c.execute("SELECT DISTINCT ticker FROM " + stocksTableName)
	return c

if (__name__ == "__main__"):
    connectToDB()
    insertStock(1,"APPL",100.01,0.001,0.5)
    insertStock(2,"APPL",200.01,0.2,0.10)
    insertTransaction("BUY",1,"XOM",200.01,100)
    insertOrder("BUY",99,"EA",11.11,11)
    getStockInfoForTicker("APPL")
    getAllTransactions()

