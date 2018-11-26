from app import app
from app.tests.class_test import UserTest
import os
import json
import pytest


#@pytest.mark.skip(reason="skip for dev test creation")
class TestSectionCRUD(object):

    userTest = UserTest()

    @pytest.fixture
    def client(self):
        client = app.test_client()
        yield client

    def test_create_section(self, client):

        data = {
            'data': {
                "name": "Platinum",
                "module_id": "5b111897bff6e228d05854b5",
                "section_start": "Start1",
                "section_end": "Start2"                
            }
        }

        url = '/create_section'
        
        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)
        assert jsonres['status_code'] == 200
        
    def test_get_section(self, client):

        data = {
            'data': {
                "name": "SectionTestDel"
            }
        }

        url = '/get_section'

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)
        jsonres['section_start'] = "UpdatedStart1"
        jsonres['section_end'] = "UpdatedEndStart"
        jsonres['section_id'] = jsonres['_id']['$oid']
        jsonres.pop('_id', None)
        self.userTest.id = jsonres['section_id']

        data = {
            'data': jsonres
        }

        url = '/update_section'
        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)
        jsonres = json.loads(res.data)

        assert jsonres['status_code'] == 200

    def test_delete_section(self, client):
        data = {
            'data': {
                "section_id": self.userTest.id
            }
        }

        url = '/delete_section'

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)

        assert jsonres['status_code'] == 200
