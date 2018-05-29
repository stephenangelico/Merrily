# Door sensor for sending a message if a door is opened
# Reference design uses a Reed switch wired as Normally Open (NO).
from gpiozero import Button
from signal import pause
import threading

import notifier
#from config import 

reed = Button(24) #TODO: Make this configurable

def test_switch():
	print("Switch closed")
	notifier.send_to_all(b'Switch closed')
	print("Notification sent")

reed.when_pressed = test_switch

notifier.start_server()
notifier.accept_conn()
