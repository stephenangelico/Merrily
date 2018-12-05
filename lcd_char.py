# Useful shortcuts for integrating a character LCD with Merrily log
# Examples also available at https://github.com/adafruit/Adafruit_Python_CharLCD
import Adafruit_CharLCD
import time
import socket
import log_server as db

lcd_rs = 16
lcd_en = 20
lcd_d4 = 6
lcd_d5 = 13
lcd_d6 = 19
lcd_d7 = 26
lcd_columns = 16
lcd_rows = 2
lcd_backlight = 4

lcd = Adafruit_CharLCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

# Basic message
lcd.message("Hello, World!")
lcd.clear()

# Show IP address
s = socket.socket()
s.connect(("192.168.0.19", 8082))
lcd.message(s.getsockname()[0])
lcd.clear()

# Show timestamp of most recent doorbell ring event
# Infinite loop warning!
while True:
	event = db.session.query(db.RingEvent).order_by(db.RingEvent.timestamp.desc()).first()
	lcd.clear()
	lcd.message("Last ring was at\n    " + event.timestamp.strftime('%H:%M:%S'))
	time.sleep(5)
