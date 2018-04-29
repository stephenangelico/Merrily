import sys
import socket
import threading
from select import select

HOST = 'localhost'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

def send_messages():
	with sock:
		while True:
			r, _, _ = select([sys.stdin, sock], [], [])
			if sys.stdin in r:
				data = input()
				sock.send(data.encode())
			if sock in r:
				data = sock.recv(1024)
				if not data:
					break
				print(data.decode())

if __name__ == '__main__':
	send_messages()
