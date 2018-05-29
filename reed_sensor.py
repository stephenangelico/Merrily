# Door sensor for sending a message if a door is opened
# Reference design uses a Reed switch wired as Normally Open (NO).
from gpiozero import Button
from signal import pause
import threading

import notifier
#from config import 

reed = Button(24) #TODO: Make this configurable

reed.when_pressed = notifier.send_to_all(b'Switch closed')

notifier.start_server()
notifier.accept_conn()

pause()
