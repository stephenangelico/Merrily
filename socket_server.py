import socket
import sys
import threading
import time
from config import DOORBELL_PORT # ImportError? See config_example.py

host = ''
port = 8090
connections = []
ring_id = 0
ring_time = time.time()
latest_ring = "Latest Ring: %r %r None" % (ring_id, ring_time)

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
			conn, addr = sock.accept() # TODO: Handle clients unexpectedly disconnecting
			print('Connecting: %s:%s' % addr)
			connections.append(conn)
			threading.Thread(target=write_socket, args=(conn, latest_ring), daemon=True).start()
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
					value = value.strip()
					if attr == "Broadcast":
						#TODO: Figure out if this client is allowed to broadcast
						if value == "Ring":
							ring(conn)
					else:
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

def ring(source):
	global ring_id
	global ring_time
	global latest_ring
	ring_id += 1
	ring_time = time.time()
	event = "Ring: %r %r %s:%s" % (ring_id, ring_time, source.getpeername()[0], source.getpeername()[1])
	latest_ring = ("Latest " + event)
	broadcast(("New " + event), source)

if __name__ == '__main__':
	start_server()
	accept_conn()
