import unittest
import os
import json
from app import create_app, db


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
    
