# Listens for doorbell signal (GPIO on RPi) and sends request to server
from gpiozero import Button
import requests

button = Button(4, bounce_time=5)

def bell_ring():
	button.wait_for_press()
	requests.post('http://f-22raptor:8088/ring')

if __name__ == '__main__':
	bell_ring()
