import socket
import sys

HOST, PORT = "codebb.cloudapp.net", 17429
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sfile = sock.makefile()
user = "Good_Biddies"
password = "asdfghjkl"
data=user + " " + password + "\n"
sock.sendall(data)

def run(user, password, *commands):

    data = "\n".join(commands) + "\n"

    sock.sendall(data)

    rline = sfile.readline()
    return rline

def subscribe(user, password):
    HOST, PORT = "codebb.cloudapp.net", 17429

    data=user + " " + password + "\nSUBSCRIBE\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()

def close():
	sock.close()

if __name__ == "__main__":
    print run("Good_Biddies", "asdfghjkl", "MY_SECURITIES")
