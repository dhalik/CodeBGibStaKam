import clientpy2
import thread
import threading
import socket
import sys
import time
import SQLService

threadRunning = False

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class subscriberThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
    	subscribe("Good_Biddies","asdfghjkl",1)

threadSubscribe = subscriberThread(1, "Thread-1", 5)

def subscribe(user, password, delay):
	print("subscribe")
	global threadRunning
	global sock
	HOST, PORT = "codebb.cloudapp.net", 17429

	data=user + " " + password + "\nSUBSCRIBE\n"

	sock.connect((HOST, PORT))
	sock.sendall(data)

	print(threadRunning)
	while threadRunning:
		time.sleep(delay)
		if not threadRunning:
			thread.exit()
			sock.close()

		try:
			sfile = sock.makefile()
			rline = sfile.readline()
			while rline:
				outputData = rline.strip()
				#Save outputData to database here
				params = outputData.split(' ');
				#Replace 0 with proper global period count later
				if len(params) == 4:
					SQLService.insertTransaction(params[0],0,params[1],params[2],params[3])
				rline = sfile.readline()
		finally:
			pass

def unsubscribeToUpdates():
	global threadRunning
	threadRunning = False

def subscribeToUpdates():
	try:
		global threadRunning
		threadRunning = True
		print(threadRunning)
		threadSubscribe.start()
	except:
		print "Error: unable to start thread"

if __name__ == "__main__":
    subscribeToUpdates()
