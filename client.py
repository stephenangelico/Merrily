import sys
import socket
import threading
from subprocess import check_call
from config import DOORBELL_SERVER, DOORBELL_PORT, PLAYER, PLAYER_ARGS, ALERT_FILE # ImportError? See config_example.py

host = DOORBELL_SERVER
port = DOORBELL_PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))
print("Connected to", host, ":", port, file=sys.stderr); sys.stderr.flush()

def wait_for_doorbell():
	with sock:
		while True:
			data = sock.recv(1024)
			if not data:
				break
			message = data.decode()
			# Use shell to run notify-send if it's a normal doorbell
			if message == 'Doorbell!':
				check_call(["notify-send", "Doorbell!", "Someone's knocking at the door!"])
				check_call([PLAYER, ALERT_FILE, PLAYER_ARGS]) # Throw an error if not available
			else:
				print(message)

if __name__ == '__main__':
	wait_for_doorbell()
