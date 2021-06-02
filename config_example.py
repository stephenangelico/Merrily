# This is an example of what should be in config.py. Save this file as config.py
# and then change the defaults as needed. See README.md for details.

# Doorbell values
A_PIN = 18
B_PIN = 23
THRESHOLD = 100
TOKEN = "" # To generate random token: `base64.b64encode(os.urandom(12)).decode("ascii")`

# Client values
DOORBELL_SERVER = "localhost"
DOORBELL_PORT = 8088
NOTIFY_COMMAND = ["notify-send", "Doorbell!", "Someone's knocking at the door!"]
PLAYER_COMMAND = ["cvlc", "ring.wav", "--play-and-exit", "--extraintf", ""]
