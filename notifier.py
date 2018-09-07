import socket
import sys
from config import DOORBELL_PORT # ImportError? See config_example.py

host = ''
port = DOORBELL_PORT
connections = []

def start_server():
	global sock
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	try:
		sock.bind((host,port))
	except socket.error as e:
		print(str(e))
		sys.exit()

	sock.listen(5)
	print("Server active on port", port)

def describe_socket(sock):
	try:
		return "%s:%s" % sock.getpeername()
	except OSError:
		return repr(sock)

def send_to_all(data):
	for connection in connections[:]:
		try:
			connection.send(bytes(data))
		except BrokenPipeError:
			# If the client loses its connection, it should restart.
			# The SystemD service file should restart the script if
			# it exited with an error anyway. Therefore, if the pipe
			# is broken, just close the connection cleanly.
			connection.close()
			connections.remove(connection)
			print("Client %s disconnected." % describe_socket(connection))

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
	start_server()
	accept_conn()
