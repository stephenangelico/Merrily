import socket
import threading
import sys

HOST = ''
PORT = 12345
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
			data = conn.recv(1024)
			send_to_all(data)
			if not data:
				print('Disconnecting: ' + str(addr[0]) + ':' + str(addr[1]))
				break
	connections.remove(conn)

def run_server():
	try:
		with sock:
			while True:
				conn, addr = sock.accept()
				connthread = threading.Thread(target=handler, args=(conn, addr))
				connthread.daemon = True
				connthread.start()
				connections.append(conn)
				print('Connected to: ' + str(addr[0]) + ':' + str(addr[1]))
	finally:
		for connection in connections:
			print(connection)
			connection.close()

if __name__ == '__main__':
	run_server()
