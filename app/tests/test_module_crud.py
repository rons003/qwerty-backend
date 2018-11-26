from app import app
from app.tests.class_test import UserTest
import os
import json
import pytest


@pytest.mark.skip(reason="skip for dev test creation")

class TestModuleCRUD(object):

    userTest = UserTest()

    @pytest.fixture
    def client(self):
        client = app.test_client()
        yield client

    def test_create_module(self, client):

        data = {
            'data': {
                "name": "ModuleTestDel",
                "desc": "ModuleTest",
                "teacher_list": ["5b050e4bab41353ab0708364", "5b050e4bab41353ab0708364"],
                "section_list": ["5b07b62bab41353ff071da5f", "5b07b62bab41353ff071da5f"]
            }
        }

        url = '/create_module'
        
        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)
        assert jsonres['status_code'] == 200

    def test_get_module(self, client):
    
        data = {
            'data': {
                "name": "ModuleTestDel"
            }
        }

        url = '/get_module'

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)
        jsonres['desc'] = "ModuleTestUpdated"
        jsonres['teacher_list'] = []
        jsonres['module_id'] = jsonres['_id']['$oid']
        jsonres.pop('_id', None)
        self.userTest.id = jsonres['module_id']

        data = {
            'data': jsonres
        }

        url = '/update_module'
        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)
        jsonres = json.loads(res.data)

        assert jsonres['status_code'] == 200

    def test_delete_section(self, client):
        data = {
            'data': {
                "module_id": self.userTest.id
            }
        }

        url = '/delete_module'

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)

        assert jsonres['status_code'] == 200

        
    
