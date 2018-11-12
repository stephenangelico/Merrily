import socket
import sys
from config import DOORBELL_PORT # ImportError? See config_example.py

host = ''
port = DOORBELL_PORT
connections = []
clients = {}

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
		return clients[sock.fileno()]
	except KeyError:
		return repr(sock)

def send_to_all(data):
	for connection in connections[:]:
		try:
			connection.send(bytes(data))
		except (BrokenPipeError, ConnectionResetError): #TODO: Handle OSError 113 No route to host
			# If the client loses its connection, it should restart.
			# The SystemD service file should restart the script if
			# it exited with an error anyway. Therefore, if the pipe
			# is broken, just close the connection cleanly.
			print("Client %s disconnected." % describe_socket(connection))
			del clients[connection.fileno()]
			connection.close()
			connections.remove(connection)

def accept_conn():
	try:
		with sock:
			while True:
				conn, addr = sock.accept()
				connections.append(conn)
				print('Connecting: %s:%s' % addr)
				clients[conn.fileno()] = "%s:%s" % addr
	finally:
		for connection in connections:
			connection.close()

if __name__ == '__main__':
	start_server()
	accept_conn()
