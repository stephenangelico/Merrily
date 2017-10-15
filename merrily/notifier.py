# Web server to run on system to be notified
# Upon reception of external doorbell signal, send a system notification
from .database import session, RingEvent, User
from merrily import app

#import json
from subprocess import call
from datetime import datetime, timedelta
#from jsonschema import validate, ValidationError
from flask import render_template, request, redirect, url_for, flash, Response
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash

PAGINATE_BY = 10

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
@app.route("/page/<int:page>")
def show_recent_events(page=1):
	# Zero-indexed page
	page_index = page - 1
	
	try:
		limit = int(request.args.get("limit", PAGINATE_BY))
	except ValueError:
		limit = PAGINATE_BY
	if limit < 1 or limit > 100:
		limit = PAGINATE_BY
	
	count = session.query(RingEvent).count()
	
	start = page_index * limit
	end = start + limit
	
	total_pages = (count - 1) // limit + 1
	has_next = page_index < total_pages - 1
	has_prev = page_index > 0
	has_paginator = True
	
	
	events = session.query(RingEvent)
	events = events.order_by(RingEvent.timestamp.desc())
	events = events[start:end]
	
	return render_template("events.html",
		events=events,
		has_next=has_next,
		has_paginator=has_paginator,
		has_prev=has_prev,
		page=page,
		total_pages=total_pages,
		limit=limit,
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

@app.route("/event/<int:id>")
def single_event(id=1):
	events = session.query(RingEvent).get(id)
	if not events:
		flash("Event not found", "warning")
		return redirect(url_for("show_recent_events"))
	return render_template("events.html",
		events=[events],
		current_user=current_user,
	)
	
@app.route("/event/<int:id>/edit", methods=["GET"])
@login_required
def edit_event_get(id):
	event = session.query(RingEvent).get(id)
	if not event:
		flash("Event not found", "warning")
		return redirect(url_for("show_recent_events"))
	return render_template("edit_event.html",
		event=event,
		current_user=current_user,
	)

@app.route("/event/<int:id>/edit", methods=["POST"])
@login_required
def edit_event_post(id):
	event = session.query(RingEvent).get(id)
	if not event:
		flash("Event not found", "warning")
		return redirect(url_for("show_recent_events"))
	event.entity=request.form["entity"]
	event.notes=request.form["notes"]
	# Shorthand for if clause to check trueness of string
	event.answered = (request.form["answered"] == "true")
	session.commit()
	return redirect(url_for("single_event", id=id))

@app.route("/event/<int:id>/delete", methods=["GET"])
@login_required
def remove_event_get(id):
	event = session.query(RingEvent).get(id)
	if not event:
		flash("Event not found", "warning")
		return redirect(url_for("show_recent_events"))
	return render_template("delete.html",
		event=event
	)
	
@app.route("/event/<int:id>/delete", methods=["POST"])
@login_required
def remove_event_post(id):
	event = session.query(RingEvent).get(id)
	if not event:
		flash("Event not found", "warning")
		return redirect(url_for("show_recent_events"))
	print("Starting deletion")
	session.query(RingEvent).filter(RingEvent.id==id).delete()
	session.commit()
	return redirect(url_for("show_recent_events"))

@app.route("/login", methods=["GET"])
def login_get():
	return render_template("login.html",
		current_user=current_user,
	)

@app.route("/login", methods=["POST"])
def login_post():
	email = request.form["email"]
	password = request.form["password"]
	user = session.query(User).filter_by(email=email).first()
	if not user or not check_password_hash(user.password, password):
		flash("Incorrect username or password", "danger")
		return redirect(url_for("login_get"))
	
	login_user(user)
	return redirect(request.args.get('next') or url_for("show_recent_events"))

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("show_recent_events"))
