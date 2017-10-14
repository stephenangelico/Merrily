import unittest
import os
#import json
from urllib.parse import urlparse

# Configure our app to use the testing database
os.environ["CONFIG_PATH"] = "merrily.config.TestingConfig"

from merrily import app
from merrily.database import Base, engine, session, RingEvent, User

class TestAPI(unittest.TestCase):
	""" Tests for Merrily web client """
	
	def setUp(self):
		""" Test setup """
		self.client = app.test_client()

		# Set up the tables in the database
		Base.metadata.create_all(engine)
	
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
		
		response = self.client.post("event/1/edit", data={
		"entity": "Someone",
		"notes": "Somewhere"
		})
		
		self.assertEqual(response.status_code, 302)
		self.assertEqual(urlparse(response.location).path, "/")
		events = session.query(RingEvent).all()
		self.assertEqual(len(events), 1)
		
		event = events[0]
		self.assertEqual(event.entity, "Someone")
		self.assertEqual(event.notes, "Somewhere")
