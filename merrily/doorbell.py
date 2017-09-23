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
def value_print():
	while True:
		print(analog_read())
		time.sleep(1)

# Main work function
def ring_listen():
	while True:
		level = analog_read()
		if level > 160:
			bell_ring()
		time.sleep(1)

# debugging function co-written by Chris Angelico
def test_listen():
	state = "idle"
	low = 200
	high = 0
	wentlow = 0
	wenthigh = 0
	while "not halted":
		level = analog_read(); t = time.time()
		if level > 150:
			if state == "idle":
				print("%17.6f Raised  %d, was %d %.6f \33[K" %(t, level, low, t - wentlow))
				state = "active"
				wenthigh = t
			high = max(high, level)
			low = 200
		else:
			if state == "active":
				print("%17.6f Lowered %d, was %d %.6f \33[K" %(t, level, high, t - wenthigh))
				state = "idle"
				wentlow = t
			low = min(low, level)
			high = 0
		print("."*(level//2 - 50), end="\33[K\r")

# Sends request to server then timeout for 5 sec to wait for sound to decay
def bell_ring():
	requests.post('http://f-22raptor:8088/ring')
	time.sleep(5)

if __name__ == '__main__':
	ring_listen()
