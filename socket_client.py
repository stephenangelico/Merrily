import socket
import sys
import subprocess
import threading
import time

from config import DOORBELL_SERVER, DOORBELL_PORT, NOTIFY_COMMAND, PLAYER_COMMAND

host = 'localhost'
port = 8090
latest_ring = {"id": 0, "timestamp": 0.0, "source": ''}
heartbeat = 0

def start_client():
	global sock
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host,port))
	print("Connected to %s:%s" % (host, port), file=sys.stderr, flush=True)

def read_socket():
	buffer = b""
	while True:
		data = sock.recv(1024)
		if not data:
			break
		buffer += data
		while b"\n" in buffer:
			line, buffer = buffer.split(b"\n", 1)
			line = line.rstrip().decode("utf-8")
			if ":" in line:
				attr, value = line.split(":", 1)
				value = value.strip()
				if attr == "Latest Ring":
					id, timestamp, source = value.split()
					try:
						id = int(id)
						timestamp = float(timestamp)
						source = str(source)
					except ValueError:
						pass # Do not overwrite latest_ring
					else:
						global latest_ring
						latest_ring["id"] = id
						latest_ring["timestamp"] = timestamp
						latest_ring["source"] = source
				elif attr == "New Ring":
					id, timestamp, source = value.split()
					try:
						id = int(id)
						timestamp = float(timestamp)
						source = str(source)
					except ValueError:
						pass # Do not ring
					else:
						if id == latest_ring["id"]:
							pass # Duplicate ring event
							# If server resets and client somehow doesn't immediately, it should either timeout
							# or get BrokenPipeError and reset.
						elif id > latest_ring["id"]:
							ring() # Clearly a new ring
						elif timestamp > (latest_ring["timestamp"] + 5):
							ring() # New ring after server reset
				elif attr == "Heartbeat":
					global heartbeat
					heartbeat = time.time()

def ring():
	subprocess.run(NOTIFY_COMMAND)
	subprocess.run(PLAYER_COMMAND) # Throw an error if not available

def heartbeat():
	while True:
		sock.send(("Heartbeat: Send\r\n").encode("utf-8"))
		time.sleep(5)
		if time.time() > (heartbeat + 5): # No response from server after 5 sec
			pass # TODO: restart the connection
		else:
			time.sleep(55)

if __name__ == '__main__':
	start_client()
	try:
		threading.Thread(target=read_socket, args=(,), daemon=True).start()
		threading.Thread(target=heartbeat, args(,), daemon=True).start()
	except KeyboardInterrupt:
		sock.close()
