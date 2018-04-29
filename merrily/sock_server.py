import socket
import sys

HOST = ''
PORT = 8088
connections = []

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	sock.bind((HOST,PORT))
except socket.error as e:
	print(str(e))
	sys.exit()

sock.listen(5)
print("Server active on port", PORT)

def send_to_all(data):
	for connection in connections:
		connection.send(bytes(data))

def handler(conn, addr):
	with conn:
		while True:
			if not data:
				print('Disconnecting: ' + str(addr[0]) + ':' + str(addr[1]))
				break
	connections.remove(conn)

def accept_conn():
	try:
		with sock:
			while True:
				conn, addr = sock.accept()
				connections.append(conn)
				print('Connecting: ' + str(addr[0]) + ':' + str(addr[1]))
	finally:
		for connection in connections:
			connection.close()

if __name__ == '__main__':
	accept_conn()
