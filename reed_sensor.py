# Door sensor for sending a message if a door is opened
# Reference design uses a Reed switch wired as Noormally Open (NO).
from gpiozero import Button
from signal import pause
import threading

import notifier
#from config import 

reed = gpiozero.Button(24) #TODO: Make this configurable

if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1] == 'testring':
		test_ring()
	else:
		notifier.start_server()
		threading.Thread(target=notifier.accept_conn).start()
		reed.when_pressed = notifier.send_to_all(b'Switch closed')
