# Web server to run on system to be notified
# Upon reception of external doorbell signal, send a system notification
import os
from flask import Flask

import json
from flask import request, Response
from jsonschema import validate, ValidationError

app = Flask(__name__)
# Copied from tuneful
#config_path = os.environ.get("CONFIG_PATH", "tuneful.config.DevelopmentConfig")
#app.config.from_object(config_path)

@app.route("/", methods=["GET"])
def wrong_path():
	# Return static HTML detailing usage
	pass

@app.route("/ring", methods=["POST"])
def notify_doorbell():
	# Use shell to run notify-send
	pass
