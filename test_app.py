import unittest
import json
from app import app
from models import db, Dancer, Event

# Tokens provided by the user
DANCER_AGENT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhiQnhKTFF4RFlCeDluWG44d3haRSJ9.eyJpc3MiOiJodHRwczovL2Fmcm9kZXYudWsuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY2ZThhMmM0NDFiZmQ0M2Q3ZGY1OTUzZSIsImF1ZCI6Imh0dHBzOi8vYWZyb2JlYXRzYWdlbmN5L2FwaSIsImlhdCI6MTcyNjY1OTA0MSwiZXhwIjoxNzI2NjY2MjQxLCJzY29wZSI6IiIsImF6cCI6IlFiNnpTVGEwMDdUZXFRQTF1NEFjaUNmUGVRcG5hbmNIIiwicGVybWlzc2lvbnMiOlsiYWRkOmRhbmNlciIsImRlbGV0ZTpkYW5jZXIiLCJlZGl0OmRhbmNlciIsImdldDpkYW5jZXItZGV0YWlscyJdfQ.ADqlKwURlRhQA6UJXfRk-E-juVQJ9A6yHkdv2ojAgGPqNTmPymGhsQDkcfAw_3jS8hVxQ3cNYuS14yu_TOWeqo7ui9oAxMrLwZVSenxUZn4Io2DMyflxH4wbyG11jzVX0xYu4mvFZKvGLMlmKwMwz80QBaybWCN-mXr2Vcl0A5LK372VtboRGorM3s5pl2WOwMnQWqb5NSOAJ4c917PHAARETnM68dsyvJiXY8VVV1vW5H8YRAjHeR-IFGhokFoINrSE-pXSAPhFgkrqjZjLGbOaG5Zv6ARhn9tMIC377NCD71NqWQMSZQ2lKVXmP7mw8wjIWF37oWDwojfqICqPmA'
EVENT_AGENT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhiQnhKTFF4RFlCeDluWG44d3haRSJ9.eyJpc3MiOiJodHRwczovL2Fmcm9kZXYudWsuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY2ZThhMjdhN2M0NGNhYmZmZTM3ZDNjYiIsImF1ZCI6Imh0dHBzOi8vYWZyb2JlYXRzYWdlbmN5L2FwaSIsImlhdCI6MTcyNjY1OTIzNCwiZXhwIjoxNzI2NjY2NDM0LCJzY29wZSI6IiIsImF6cCI6IlFiNnpTVGEwMDdUZXFRQTF1NEFjaUNmUGVRcG5hbmNIIiwicGVybWlzc2lvbnMiOlsiYWRkOmV2ZW50IiwiZGVsZXRlOmV2ZW50IiwiZWRpdDpldmVudCIsImdldDpldmVudC1kZXRhaWxzIl19.eoD8l_LFSL8-pv2aNmJTO0DE89v-rSOoQDolhCPHCYID46HREXKKKQ7a_7b-FuxrLcgZa8408pWSGMZTtLK15HJjBN7hIcrNHwMnf6k7UtYktJ33bvKCFv61D2j7MKsKn_vVbED6ta7HhAQ9wgtB_Jp5YLCf_QXybBMtJaw1a8Y1adXIzPLoK9J9pLOoX_DIDTlhcDlXPNTPlFM7u6KeERzfM6oBRewALcereEltp7fcIN9kVQ0VWjC6YaA82VVBRcFmo_N2N37EQFRub0J_pq8lEfX9pk5MHXOfekI9sYv6A7nHtRljkAXz1F5qmi_b_9kNDr1UIeVQ9hbc7u7LMg'
DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhiQnhKTFF4RFlCeDluWG44d3haRSJ9.eyJpc3MiOiJodHRwczovL2Fmcm9kZXYudWsuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY2ZTlmZTVmMjFjNTFkYWUzMGMyMDIzMyIsImF1ZCI6Imh0dHBzOi8vYWZyb2JlYXRzYWdlbmN5L2FwaSIsImlhdCI6MTcyNjY1OTMwNiwiZXhwIjoxNzI2NjY2NTA2LCJzY29wZSI6IiIsImF6cCI6IlFiNnpTVGEwMDdUZXFRQTF1NEFjaUNmUGVRcG5hbmNIIiwicGVybWlzc2lvbnMiOlsiYWRkOmRhbmNlciIsImFkZDpldmVudCIsImRlbGV0ZTpkYW5jZXIiLCJkZWxldGU6ZXZlbnQiLCJlZGl0OmRhbmNlciIsImVkaXQ6ZXZlbnQiLCJnZXQ6ZGFuY2VyLWRldGFpbHMiLCJnZXQ6ZXZlbnQtZGV0YWlscyJdfQ.MFP1_60M_9Kq2cAXL58P9W8IOXsqMXH5RKsXyqXzwdJMCHL_YudznZdcExCOOryhX2fwKqwT8RaxZLXknI_-y-Gy5h_mq7E61Lzi6o5DoID9dJaehn_qLUV24r4b6pSDHnGrG7GSlcLM-wVOJKeTRNeLCUnN0jXHnrh5AySpJbBSSMFfldguM-WGl0wpnBCFxq9Q--n2TT5OntDmblDNnfQOVpVrPBXNs3oqnxks6C07_mb-DFKRZScUprSnB0N5MV4zbUsbWnomRgp2WNOp1UVlxcRC-saGv-gxaoI3MAnhSuIZ4Wl_IUnzNFUb1u9hjQbRfnLm5bQX4WGCM45fEw'


class AgencyTestCase(unittest.TestCase):
    """This class represents the test case for the agency application"""

    def setUp(self):
        """Define test variables and initialize the app"""
        # Create the Flask app using the factory function
       
        self.client = app.test_client
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}/{}".format('localhost:5432', 'agency_test')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        
        with app.app_context():
            db.create_all()  
   

        # Example data to test with
        self.new_dancer = {
            'name': 'Test Dancer',
            'age': 25,
            'gender': 'female',
            'phone': '123456789',
            'website': 'http://testdancer.com'
        }
        
        self.new_event = {
            'name': 'Test Event',
            'date': '2024-12-31',
            'location': 'Test City'
        }

        # Set headers for each role
        self.dancer_headers = {'Authorization': f'Bearer {DANCER_AGENT_TOKEN}'}
        self.event_headers = {'Authorization': f'Bearer {EVENT_AGENT_TOKEN}'}
        self.director_headers = {'Authorization': f'Bearer {DIRECTOR_TOKEN}'}

    def tearDown(self):
        """Executed after each test"""
        with app.app_context():
            db.session.remove()  # Remove the session
            db.drop_all()  # Drop all tables

    # Tests for Dancer Endpoints
    def test_get_dancers_success(self):
        res = self.client().get('/dancers')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_get_dancers_failure(self):
        res = self.client().get('/dancers', headers={'Authorization': 'Bearer invalidtoken'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_add_dancer_success(self):
        res = self.client().post('/dancers', json=self.new_dancer, headers=self.director_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])

    def test_add_dancer_failure(self):
        res = self.client().post('/dancers', json={}, headers=self.director_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    # Tests for Event Endpoints
    def test_get_events_success(self):
        res = self.client().get('/events')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_add_event_fail(self):
        res = self.client().post('/events', json=self.new_event, headers=self.director_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_add_event_failure(self):
        res = self.client().post('/events', json={}, headers=self.director_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    # RBAC Tests
    def test_add_dancer_dancer_agent_permission_denied(self):
        res = self.client().post('/dancers', json=self.new_dancer, headers=self.event_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)  # Should fail due to lack of permission
        self.assertFalse(data['success'])

    def test_add_event_event_agent_permission_denied(self):
        res = self.client().post('/events', json=self.new_event, headers=self.dancer_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)  # Should fail due to lack of permission
        self.assertFalse(data['success'])

if __name__ == "__main__":
    unittest.main()
