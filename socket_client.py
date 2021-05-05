import socket
import sys
import subprocess
import threading
import time

from config import DOORBELL_SERVER, DOORBELL_PORT, NOTIFY_COMMAND, PLAYER_COMMAND

host = 'localhost'
port = 8090

class Conn(object):
	latest_ring = {"id": 0, "timestamp": 0.0, "source": ''}
	heartbeat = True

	def __init__(self):
		self.connect()
		threading.Thread(target=self.read_socket, daemon=True).start()
		self.server_lost = threading.Event()
		self.keepalive()

	def connect(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((host,port))
		print("Connected to %s:%s" % (host, port), file=sys.stderr, flush=True)

	def read_socket(self):
		buffer = b""
		while True:
			data = self.sock.recv(1024)
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
							self.latest_ring["id"] = id
							self.latest_ring["timestamp"] = timestamp
							self.latest_ring["source"] = source
					elif attr == "New Ring":
						id, timestamp, source = value.split()
						try:
							id = int(id)
							timestamp = float(timestamp)
							source = str(source)
						except ValueError:
							pass # Do not ring
						else:
							if id == self.latest_ring["id"]:
								pass # Duplicate ring event
								# If server resets and client somehow doesn't immediately, it should either timeout
								# or get BrokenPipeError and reset.
							elif id > self.latest_ring["id"]:
								self.ring() # Clearly a new ring
							elif timestamp > (self.latest_ring["timestamp"] + 5):
								self.ring() # New ring after server reset
					elif attr == "Heartbeat":
						self.heartbeat = True
						print("Heartbeat")
		self.server_lost.set()

	def ring(self):
		subprocess.run(NOTIFY_COMMAND)
		subprocess.run(PLAYER_COMMAND) # Throw an error if not available

	def keepalive(self):
		while self.heartbeat:
			self.heartbeat = False
			self.sock.send(("Heartbeat: Send\r\n").encode("utf-8"))
			print("Heartbeat sent")
			if self.server_lost.wait(10):
				break
		self.quit()

	def quit(self):
		self.sock.close()

if __name__ == '__main__':
	try:
		while True:
			try:
				conn = Conn()
			except ConnectionRefusedError:
				#TODO: Be less noisy
				print("Lost connection to server")
				time.sleep(5)
	except KeyboardInterrupt:
		pass # Quit quietly
