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

@app.route("/entry/<int:id>")
def single_event(id=1):
	#TODO: default to latest event instead of first one
	events = session.query(RingEvent).get(id)
	return render_template("events.html",
		events=[events]
	)
	
@app.route("/entry/<int:id>/edit", methods=["GET"])
#@login_required
def edit_event_get(id):
	#TODO: add Edit (and delete) links in DOM
	event = session.query(RingEvent).get(id)
	return render_template("edit_event.html",
		event=event
	)

@app.route("/entry/<int:id>/edit", methods=["POST"])
#@login_required
def edit_event_post(id):
	event = session.query(RingEvent).get(id)
	event.entity=request.form["entity"]
	event.notes=request.form["notes"]
	# Shorthand for if clause to check trueness of string
	event.answered=(request.form["answered"] == "true")
	session.commit()
	return redirect(url_for("single_event", id=id))

#TODO: add function for deleting entries


