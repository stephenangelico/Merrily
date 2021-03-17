import socket
import sys
import threading
from config import DOORBELL_PORT # ImportError? See config_example.py

host = ''
port = 8090

def start_server():
	global sock
	sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	try:
		sock.bind((host,port))
	except socket.error as e:
		print(str(e))
		sys.exit()

	sock.listen(5)
	print("Server active on port", port)

def accept_conn():
	with sock:
		while True:
			conn, addr = sock.accept()
			print('Connecting: %s:%s' % addr)
			conn.close()

if __name__ == '__main__':
	start_server()
	accept_conn()
