import unittest
import json
from usrmgr import create_app, db


class UserTestCase(unittest.TestCase):
    """These are the tests for the users api"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.testuser = {
            'first_name': 'Daniel',
            'last_name': 'Salinas',
            'userid': 'imsplitbit',
        }

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        """Test API can create a user (POST)"""
        res = self.client().post('/users/', data=self.testuser)
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(self.testuser['first_name'],
                         data['result']['first_name'])
