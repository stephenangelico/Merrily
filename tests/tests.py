import unittest
import os
#import json
from urllib.parse import urlparse
from werkzeug.security import generate_password_hash

# Configure our app to use the testing database
os.environ["CONFIG_PATH"] = "merrily.config.TestingConfig"

from merrily import app
from merrily.database import Base, engine, session, RingEvent, User

class ServerTests(unittest.TestCase):
	""" Tests for Merrily web client """
	
	def setUp(self):
		""" Test setup """
		self.client = app.test_client()

		# Set up the tables in the database
		Base.metadata.create_all(engine)
		
		# Create an example user
		self.user = User(name="Alice", email="alice@example.com",
				password=generate_password_hash("test"))
		session.add(self.user)
		session.commit()
	
	def simulate_login(self):
		with self.client.session_transaction() as http_session:
			http_session["user_id"] = str(self.user.id)
			http_session["_fresh"] = True

	def tearDown(self):
		""" Test teardown """
		session.close()
		# Remove the tables and their data from the database
		Base.metadata.drop_all(engine)
	
	def test_add_event(self):
		response = self.client.post("/ring")
		
		self.assertEqual(response.status_code, 200)
		events = session.query(RingEvent).all()
		self.assertEqual(len(events), 1)
	
	def test_edit_event(self):
		self.test_add_event()
		self.simulate_login()
		
		response = self.client.post("/event/1/edit", data={
			"entity": "Someone",
			"notes": "Somewhere",
			"answered": "true",
		})
		
		self.assertEqual(response.status_code, 302)
		self.assertEqual(urlparse(response.location).path, "/event/1")
		events = session.query(RingEvent).all()
		self.assertEqual(len(events), 1)
		
		event = events[0]
		self.assertEqual(event.entity, "Someone")
		self.assertEqual(event.notes, "Somewhere")
		self.assertEqual(event.answered, True)
	
	def test_empty_field(self):
		self.test_add_event()
		self.simulate_login()
		
		response = self.client.post("/event/1/edit", data={
			"entity": "",
			"notes": "Somewhere",
			"answered": "true",
		})
		
		self.assertEqual(response.status_code, 302)
		self.assertEqual(urlparse(response.location).path, "/event/1")
		events = session.query(RingEvent).all()
		self.assertEqual(len(events), 1)
		
		event = events[0]
		self.assertEqual(event.entity, "")
	
	def test_long_values(self):
		self.test_add_event()
		self.simulate_login()
		
		response = self.client.post("/event/1/edit", data={
			"entity": "Someone "*17,
			"notes": "Somewher"*129,
			"answered": "true",
		})
		
		self.assertEqual(response.status_code, 302)
		self.assertEqual(urlparse(response.location).path, "/event/1")
		events = session.query(RingEvent).all()
		self.assertEqual(len(events), 1)
		
		event = events[0]
		self.assertEqual(event.entity, ("Someone "*17)[:127])
		self.assertEqual(event.notes, ("Somewher"*129)[:1023])
		self.assertEqual(event.answered, True)
	
	def test_delete_event(self):
		self.test_add_event()
		self.simulate_login()
		
		response = self.client.post("/event/1/delete")
		
		self.assertEqual(response.status_code, 302)
		self.assertEqual(urlparse(response.location).path, "/")
		events = session.query(RingEvent).all()
		self.assertEqual(len(events), 0)
