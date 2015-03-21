#SQL DB
import sqlite3
import string

dbName = 'gibstankam.db'
tableName = 'stocks'

def connectToDB():
	conn = sqlite3.connect(dbName)
	c = conn.cursor()
	# Create table
	c.execute('DROP TABLE if exists stocks')
	c.execute('''CREATE TABLE stocks
	             (period integer, ticker text, networth double, dividendratio double, volatility double)''')

	# Save (commit) the changes
	conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()

def getStockInfoForTicker(ticker):
	t = (ticker,)
	conn = sqlite3.connect(dbName)
	c = conn.cursor()
	c.execute('SELECT * FROM stocks WHERE ticker=?', t)
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
	# Insert a row of data
	c.execute("INSERT INTO " + tableName + " VALUES ('" + str(period) + "','" + ticker +"','"+ str(networth) + "','"+str(dividendratio)+ "','"+ str(volatility) + "')")
	conn.commit()
	conn.close()


connectToDB()
insertStock(1,"APPL",100.01,0.001,0.5)
insertStock(2,"APPL",200.01,0.2,0.10)
getStockInfoForTicker("APPL")

