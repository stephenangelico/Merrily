import sys
import socket
import threading
from subprocess import call

HOST = 'f-18hornet'
PORT = 8088

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

def wait_for_doorbell():
	with sock:
		while True:
			data = sock.recv(1024)
			if not data:
				break
			message = data.decode()
			# Use shell to run notify-send if it's a normal doorbell
			if message == 'Doorbell!':
				call(["notify-send", "Doorbell!", "Someone's knocking at the door!"])
			else:
				print(message)

if __name__ == '__main__':
	wait_for_doorbell()
