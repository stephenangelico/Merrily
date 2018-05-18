# Web server to run in parallel to doorbell machine
# Can run on completely separate machine if desired

# Standard library stuff
import os
import sys
from datetime import datetime, timedelta
# Flask web server
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin
from werkzeug.security import check_password_hash
# DB backend
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# Local config
import config

# App init
app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "config.DevelopmentConfig")
app.config.from_object(config_path)

# DB init
engine = create_engine(app.config["DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class RingEvent(Base):
	__tablename__ = "ringevents"
	
	id = Column(Integer, primary_key=True)
	timestamp = Column(DateTime, default=datetime.now)
	entity = Column(String(128))
	notes = Column(String(1024))
	answered = Column(Boolean, default=False)

class User(Base, UserMixin):
	__tablename__ = "users"
	
	id = Column(Integer, primary_key=True)
	name = Column(String(128))
	email = Column(String(128), unique=True)
	password = Column(String(128))

Base.metadata.create_all(engine)

# Global for web display
PAGINATE_BY = 10

# Login handler
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login_get"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))

# Display filters
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

# Web endpoints
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
	checkentity = request.form["entity"]
	checkentity = checkentity[:127]
	checknotes = request.form["notes"]
	checknotes = checknotes[:1023]
	event.entity=checkentity
	event.notes=checknotes
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

# Execution functions
def run():
    port = int(os.environ.get('PORT', 8089))
    app.run(host='0.0.0.0', port=port)

def adduser():
	from getpass import getpass
	from werkzeug.security import generate_password_hash
	name = input("Name: ")
	email = input("Email: ")
	if session.query(User).filter_by(email=email).first():
		print("User with that email address already exists")
		return
	
	password = ""
	while len(password) < 8 or password != password_2:
		password = getpass("Password: ")
		password_2 = getpass("Re-enter password: ")
	user = User(name=name, email=email,
			password=generate_password_hash(password))
	session.add(user)
	session.commit()

if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1] == 'adduser':
		adduser()
	else:
		run()
