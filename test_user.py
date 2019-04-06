import unittest
import json
from copy import deepcopy
from usrmgr import create_app
from usrmgr.models import db


class UserTestCase(unittest.TestCase):
    """These are the tests for the users api"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.testuserid = 'imsplitbit'
        self.testuser = {
            'first_name': 'Daniel',
            'last_name': 'Salinas'
        }

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def add_testuser(self):
        res = self.client().post(
            '/api/v0/users/{}'.format(self.testuserid,), data=self.testuser)
        self.assertEqual(res.status_code, 201)
        return res

    def test_user_creation(self):
        """Test API can create a user (POST)"""
        data = json.loads(self.add_testuser().data)
        self.assertEqual(self.testuser['first_name'],
                         data['results']['first_name'])

    def test_user_creation_failures(self):
        """Test API user creation failure cases"""
        self.add_testuser()
        res = self.client().post(
            '/api/v0/users/{}'.format(self.testuserid), data=self.testuser)
        self.assertEqual(res.status_code, 409)

    def test_list_users(self):
        """Test API can list users"""
        self.add_testuser()
        res = self.client().get('/api/v0/users')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['results'][0]['userid'], self.testuserid)

    def test_list_user(self):
        """Test API can list a user"""
        self.add_testuser()
        res = self.client().get('/api/v0/users/{}'.format(self.testuserid))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['results']['userid'], self.testuserid)

    def test_list_user_failures(self):
        """Test API list user failure cases"""
        res = self.client().get('/api/v0/users/baduser')
        self.assertEqual(res.status_code, 404)

    def test_modify_user(self):
        """Test API allows users to be modified"""
        usermod = {
            'userid': 'dsal',
            'first_name': 'Daniel',
            'last_name': 'Salinas'
        }
        self.add_testuser()
        res = self.client().put(
            '/api/v0/users/{}'.format(self.testuserid,), data=usermod)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['results']['userid'], usermod['userid'])

    def test_modify_user_failures(self):
        """Test API user modification failure cases"""
        res = self.client().put('/api/v0/users/baduser')
        self.assertEqual(res.status_code, 404)

    def test_delete_user(self):
        """Test API allows users to be deleted"""
        self.add_testuser()
        res = self.client().delete(
            '/api/v0/users/{}'.format(self.testuserid,))
        self.assertEqual(res.status_code, 200)

    def test_delete_user_failures(self):
        """Test API delete user failure cases"""
        res = self.client().delete('/api/v0/users/baduser')
        self.assertEqual(res.status_code, 404)
