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
			#TODO: start tracking latest Ring event and send on client connection
			threading.Thread(target=write_socket, args=(conn, "Hello: world"), daemon=True).start()

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

if __name__ == '__main__':
	start_server()
	accept_conn()
