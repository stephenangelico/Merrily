# Web server to run on system to be notified
# Upon reception of external doorbell signal, send a system notification
#import os
#from flask import Flask
from .database import session, RingEvent
from merrily import app

import json
from flask import request, Response
from subprocess import call
#from jsonschema import validate, ValidationError

#app = Flask(__name__)
# Copied from tuneful
#config_path = os.environ.get("CONFIG_PATH", "merrily.config.DevelopmentConfig")
#app.config.from_object(config_path)

@app.route("/", methods=["GET"])
def wrong_path():
	# Return static HTML detailing usage
	pass

@app.route("/ring", methods=["POST"])
def notify_doorbell():
	# Use shell to run notify-send
	call(["notify-send", "Doorbell!", "Someone's knocking at the door!"])
	# Add event to database
	ring = RingEvent() #Needs no data
	return Response("Done", 200, mimetype="text/plain")

#TODO: add endpoints for editing event details
