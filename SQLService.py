#SQL DB
import sqlite3
import string

dbName = 'gibstankam.db'
stocksTableName = 'stocks'
transactionsTableName = 'transactions'

def connectToDB():
	conn = sqlite3.connect(dbName)
	c = conn.cursor()
	# Create table
	c.execute("DROP TABLE if exists " + stocksTableName + "")
	c.execute("DROP TABLE if exists " + transactionsTableName + "")

	c.execute("CREATE TABLE " + stocksTableName + "(period integer, ticker text, networth double, dividendratio double, volatility double)")
	# c.execute('''CREATE TABLE stocks
	#              (period integer, ticker text, networth double, dividendratio double, volatility double)''')
	c.execute("CREATE TABLE " + transactionsTableName + "(type text, period integer,ticker text, price double, shares integer)")
	# Save (commit) the changes
	conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()

def getStockInfoForTicker(ticker):
	t = (ticker,)
	conn = sqlite3.connect(dbName)
	c = conn.cursor()
	c.execute("SELECT * FROM " + stocksTableName+ " WHERE ticker=?", t)
	print c.fetchall()
	conn.commit()
	conn.close()

#Only use this if you are really friggin lazy...
def getStockInfoForQuery(query):
	conn = sqlite3.connect(dbName)
	c = conn.cursor()
	c.execute(query)
	conn.commit()
	conn.close()

def insertStock(period,ticker,networth,dividendratio,volatility):
	conn = sqlite3.connect(dbName)
	c = conn.cursor()
	c.execute("INSERT INTO " + stocksTableName 
		+ " VALUES ('" + str(period) + "','" + ticker +"','"+ str(networth) + "','"+str(dividendratio)+ "','"+ str(volatility) + "')")
	conn.commit()
	conn.close()

def getAllTransactions():
	conn = sqlite3.connect(dbName)
	c = conn.cursor()
	c.execute("SELECT * FROM " + transactionsTableName)
	print c.fetchall()
	conn.commit()
	conn.close()

def insertTransaction(transType, period, ticker, price, shares):
	conn = sqlite3.connect(dbName)
	c = conn.cursor()
	c.execute("INSERT INTO " + transactionsTableName 
		+ " VALUES ('" + str(transType) + str(period) + "','" + str(ticker) + "','" + str(price) +"','"+ str(shares) + "')")
	conn.commit()
	conn.close()

connectToDB()
insertStock(1,"APPL",100.01,0.001,0.5)
insertStock(2,"APPL",200.01,0.2,0.10)
insertTransaction(1,"APPL",200.01,100)
getStockInfoForTicker("APPL")
getAllTransactions()

