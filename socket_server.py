import socket
import sys
import threading
from config import DOORBELL_PORT # ImportError? See config_example.py

host = ''
port = 8090
connections = []

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
			connections.append(conn)
			#TODO: start tracking latest Ring event and send on client connection
			threading.Thread(target=write_socket, args=(conn, "Hello: world"), daemon=True).start()
			threading.Thread(target=read_socket, args=(conn,), daemon=True).start()
			

def close_conn(conn):
	print('Disconnecting: %s:%s' % conn.getpeername())
	conn.close()
	if conn in connections:
		connections.remove(conn)

def read_socket(conn):
	buffer = b""
	with conn:
		while True:
			data = conn.recv(1024)
			if not data:
				break
			buffer += data
			while b"\n" in buffer:
				line, buffer = buffer.split(b"\n", 1)
				line = line.rstrip().decode("utf-8")
				if ":" in line:
					attr, value = line.split(":", 1)
					print("Attr:", attr)
					print("Value:", value)
				else:
					print(line)

def write_socket(conn, message):
	message += "\r\n"
	data = message.encode("utf-8")
	conn.send(data)
	#TODO: handle various errors including lost connections

def broadcast(message, source=None):
	recipients = connections[:] # Sliced to allow free manipulation of connections list if necessary
	if source in recipients:
		recipients.remove(source)
	for conn in recipients:
		write_socket(conn, message)

if __name__ == '__main__':
	start_server()
	accept_conn()
