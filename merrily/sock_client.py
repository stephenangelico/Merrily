import socket
import threading

HOST = 'localhost'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))
def send_messages():
	with sock:
		while True:
			sock.send(input("").encode())

def get_messages():
	while True:
		data = sock.recv(1024)
		if not data:
			break
		print(data.decode())

if __name__ == '__main__':
	thrd = threading.Thread(target=get_messages)
	thrd.daemon = True
	thrd.start()
	send_messages()
