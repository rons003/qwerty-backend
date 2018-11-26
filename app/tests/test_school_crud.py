from app import app
from app.tests.class_test import UserTest
import os
import json
import pytest


#@pytest.mark.skip(reason="skip for dev test creation")

class TestSchoolCRUD(object):

    userTest = UserTest()

    @pytest.fixture
    def client(self):
        client = app.test_client()
        yield client

    def test_create_school(self, client):

        data = {
            'data' : {
            "name": "Fatima",
            "address": "Pasig",
            "teachers": ["Two","One"],
            "administrator_id": "5aeac511bff6e241780a4b77"
            }
        }

        url = '/upsert_school'
    
        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)      
        assert jsonres['status_code'] == 200
        
    def test_get_school(self, client):
        
        data = {
            'data' : {
            "name": "Fatima"
            }
        }

        url = '/get_school'

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)    
        jsonres['admins'] = ["UpdatedAdmin1","UpdatedAmid2"]        
        jsonres['school_id'] = jsonres['_id']['$oid']
        jsonres.pop('_id',None)
        self.userTest.id = jsonres['school_id']

        data = {
            'data': jsonres
        }
        
        url = '/update_school'
        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)
        jsonres = json.loads(res.data)
        
        assert jsonres['status_code'] == 200

    
    def test_delete_school(self, client):
        data = {
            'data' : {
                "school_id": self.userTest.id
            }
        }

        url = '/delete_school'

        res = client.post(url, data=json.dumps(
             data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)

        assert jsonres['status_code'] == 200

    
    

