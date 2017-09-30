# Web server to run on system to be notified
# Upon reception of external doorbell signal, send a system notification
from .database import session, RingEvent
from merrily import app

#import json
from subprocess import call
from datetime import datetime, timedelta
#from jsonschema import validate, ValidationError
from flask import render_template, request, redirect, url_for, flash, Response
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash

@app.template_filter()
def timeformat(timestamp, format):
	if not timestamp:
		return None
	return timestamp.strftime(format)

@app.template_filter()
def boolean_yesno(boolean):
	if boolean:
		return "Yes"
	else:
		return "No"

@app.route("/")
def show_recent_events():
	# Show ring events from the last 24 hours
	events = session.query(RingEvent).filter(RingEvent.timestamp > (datetime.now() - timedelta(hours=24)))
	events = events.order_by(RingEvent.timestamp.desc())
	
	return render_template("events.html",
		events=events,
		current_user=current_user,
		)

@app.route("/ring", methods=["POST"])
def notify_doorbell():
	# Use shell to run notify-send
	call(["notify-send", "Doorbell!", "Someone's knocking at the door!"])
	# Add event to database
	ring = RingEvent() #Needs no data
	session.add(ring)
	session.commit()
	return Response("Done", 200, mimetype="text/plain")

#TODO: add endpoints for editing event details
