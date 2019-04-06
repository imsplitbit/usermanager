import unittest
import json
from usrmgr import create_app
from usrmgr.models import db


class GroupTestCase(unittest.TestCase):
    """These are the tests for the groups api"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.testgroupid = 'admins'

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def add_testgroup(self):
        res = self.client().post('/api/v0/groups/{}'.format(self.testgroupid))
        self.assertEqual(res.status_code, 201)
        return res

    def test_group_creation(self):
        """Test API group creation"""
        data = json.loads(self.add_testgroup().data)
        self.assertEqual(data['results']['groupid'], self.testgroupid)

    def test_group_creation_failures(self):
        """Test API group creation failure cases"""
        self.add_testgroup()
        res = self.client().post('/api/v0/groups/{}'.format(self.testgroupid,))
        self.assertEqual(res.status_code, 409)

    def test_group_deletion(self):
        """Test API group delete operation"""
        self.add_testgroup()
        res = self.client().delete(
            '/api/v0/groups/{}'.format(self.testgroupid,))
        self.assertEqual(res.status_code, 200)

    def test_group_deletion_failures(self):
        """Test API group delete failure cases"""
        res = self.client().delete(
            '/api/v0/groups/{}'.format(self.testgroupid,))
        self.assertEqual(res.status_code, 404)

    def test_group_modification(self):
        """Test API group modification"""
        groupmod = {
            'groupid': 'superadmins'
        }
        self.add_testgroup()
        res = self.client().put(
            '/api/v0/groups/{}'.format(self.testgroupid,), data=groupmod)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['results']['groupid'], groupmod['groupid'])

    def test_group_modification_failures(self):
        """Test API group modification failure cases"""
        res = self.client().put(
            '/api/v0/groups/{}'.format(self.testgroupid,), data={})
        self.assertEqual(res.status_code, 404)

    def test_list_all_groups(self):
        """Test API full group listing"""
        res = self.client().post('/api/v0/groups/group1')
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v0/groups/group2')
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v0/groups/group3')
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v0/groups')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['results']), 3)

    def test_list_group(self):
        """Test API individual group listing"""
        self.add_testgroup()
        res = self.client().get('/api/v0/groups/{}'.format(self.testgroupid,))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['results']['groupid'], self.testgroupid)

    def test_list_group_failures(self):
        """Test API individual group listing failure cases"""
        res = self.client().get('/api/v0/groups/{}'.format(self.testgroupid,))
        self.assertEqual(res.status_code, 404)
