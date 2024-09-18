import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import setup_db, Dancer, Event

class AfroBeatsAgencyTestCase(unittest.TestCase):
    """This class represents the AfroBeatsAgency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "afrobeats_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Set up tokens for different roles
        self.director_token = os.getenv('DIRECTOR_TOKEN')  # Director token
        self.dancer_agent_token = os.getenv('DANCER_AGENT_TOKEN')  # Dancer agent token
        self.events_agent_token = os.getenv('EVENTS_AGENT_TOKEN')  # Events agent token

        # Sample payloads for adding/updating resources
        self.new_dancer = {
            "name": "John Doe",
            "age": 25,
            "gender": "male",
            "phone": "123-456-7890",
            "website": "http://example.com"
        }

        self.new_event = {
            "name": "Afro Beats Night",
            "address": "123 Party Street",
            "date": "2024-12-31"
        }

        self.updated_dancer = {
            "name": "John Smith",
            "age": 30,
            "gender": "male",
            "phone": "987-654-3210",
            "website": "http://example-updated.com"
        }

        self.updated_event = {
            "name": "Afro Beats Gala",
            "address": "456 Festival Ave",
            "date": "2024-11-11"
        }

    def tearDown(self):
        """Executed after each test"""
        pass

    # Utility method to set headers with appropriate JWT token
    def set_auth_headers(self, token):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

    # Test cases for the /dancers endpoint
    def test_get_dancers(self):
        res = self.client().get('/dancers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['dancers']) > 0)

    def test_404_get_dancer_details(self):
        res = self.client().get('/dancers/999999', headers=self.set_auth_headers(self.dancer_agent_token))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_add_dancer(self):
        res = self.client().post('/dancers', headers=self.set_auth_headers(self.dancer_agent_token), json=self.new_dancer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertTrue(data['dancer'])

    def test_401_add_dancer_without_auth(self):
        res = self.client().post('/dancers', json=self.new_dancer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_update_dancer(self):
        # First add a dancer
        res = self.client().post('/dancers', headers=self.set_auth_headers(self.dancer_agent_token), json=self.new_dancer)
        dancer_id = json.loads(res.data)['dancer']['id']

        # Now update the dancer
        res = self.client().patch(f'/dancers/{dancer_id}', headers=self.set_auth_headers(self.dancer_agent_token), json=self.updated_dancer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_404_update_non_existent_dancer(self):
        res = self.client().patch('/dancers/999999', headers=self.set_auth_headers(self.dancer_agent_token), json=self.updated_dancer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_dancer(self):
        # First add a dancer
        res = self.client().post('/dancers', headers=self.set_auth_headers(self.dancer_agent_token), json=self.new_dancer)
        dancer_id = json.loads(res.data)['dancer']['id']

        # Now delete the dancer
        res = self.client().delete(f'/dancers/{dancer_id}', headers=self.set_auth_headers(self.dancer_agent_token))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_404_delete_non_existent_dancer(self):
        res = self.client().delete('/dancers/999999', headers=self.set_auth_headers(self.dancer_agent_token))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # Test cases for the /events endpoint
    def test_get_events(self):
        res = self.client().get('/events')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['events']) > 0)

    def test_404_get_event_details(self):
        res = self.client().get('/events/999999', headers=self.set_auth_headers(self.events_agent_token))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_add_event(self):
        res = self.client().post('/events', headers=self.set_auth_headers(self.events_agent_token), json=self.new_event)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertTrue(data['event'])

    def test_401_add_event_without_auth(self):
        res = self.client().post('/events', json=self.new_event)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_update_event(self):
        # First add an event
        res = self.client().post('/events', headers=self.set_auth_headers(self.events_agent_token), json=self.new_event)
        event_id = json.loads(res.data)['event']['id']

        # Now update the event
        res = self.client().patch(f'/events/{event_id}', headers=self.set_auth_headers(self.events_agent_token), json=self.updated_event)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_404_update_non_existent_event(self):
        res = self.client().patch('/events/999999', headers=self.set_auth_headers(self.events_agent_token), json=self.updated_event)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_event(self):
        # First add an event
        res = self.client().post('/events', headers=self.set_auth_headers(self.events_agent_token), json=self.new_event)
        event_id = json.loads(res.data)['event']['id']

        # Now delete the event
        res = self.client().delete(f'/events/{event_id}', headers=self.set_auth_headers(self.events_agent_token))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_404_delete_non_existent_event(self):
        res = self.client().delete('/events/999999', headers=self.set_auth_headers(self.events_agent_token))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

    #pip install unittest
    # python tests.py