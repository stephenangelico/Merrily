# Forked from https://github.com/simonmonk/raspberrypi_cookbook_ed2 pot_step.py
# Used here with 100KΩ resistors, 10nF capacitor and doorbell line out,
# whereas original recipe used 1K resistors, 220nF capacitor and 10KΩ trimpot.
#
# Original copyright notice:
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Simon Monk
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

####################################
#         Analog Read Code         #
#         by Simon Monk            #
#         modified by Don Wilcher  #
#         Jan 1/31/15              #
####################################

# include RPi libraries in to Python code
import RPi.GPIO as GPIO
import time
import requests

# instantiate GPIO as an object
GPIO.setmode(GPIO.BCM)

# define GPIO pins with variables a_pin and b_pin
a_pin = 18
b_pin = 23

# create discharge function for reading capacitor data
def discharge():
	GPIO.setup(a_pin, GPIO.IN)
	GPIO.setup(b_pin, GPIO.OUT)
	GPIO.output(b_pin, False)
	time.sleep(0.005)

# create time function for capturing analog count value
def charge_time():
	GPIO.setup(b_pin, GPIO.IN)
	GPIO.setup(a_pin, GPIO.OUT)
	count = 0
	GPIO.output(a_pin, True)
	while not GPIO.input(b_pin):
		count = count +1
	return count

# create analog read function for reading charging and discharging data
def analog_read():
	discharge()
	return charge_time()

# provide a loop to display analog data count value on the screen
def ring_listen():
	while True:
		level = analog_read()
		if level > 180:
			bell_ring()
		time.sleep(1)

# Sends request to server then timeout for 5 sec to wait for sound to decay
def bell_ring():
	requests.post('http://f-22raptor:8088/ring')
	time.sleep(5)

if __name__ == '__main__':
	ring_listen()
