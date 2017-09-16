# Listens for doorbell signal (GPIO on RPi) and sends request to server
from gpiozero import Button
import requests
import time

button = Button(26)

def bell_ring():
	button.wait_for_press()
	requests.post('http://f-22raptor:8088/ring')
	time.sleep(5)

while __name__ == '__main__':
	bell_ring()
