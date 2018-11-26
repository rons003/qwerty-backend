from app import app
from app.tests.class_test import UserTest
import os, json
import pytest


@pytest.mark.skip(reason="skip for dev test creation")

class TestSignIn(object):

    userTest = UserTest()

    @pytest.fixture
    def client(self):    
        client = app.test_client()    
        yield client

    def test_signin_and_update(self,client):    
        data = {
            'data': {
            'username': 'admin',
            'pwd': 'admin'
            }
        }

        url = '/signin'
        
        res = client.post(url, data=json.dumps(data), headers=self.userTest.headers)
        
        jsonres = json.loads(res.data)
        userdata = jsonres['user']
        userdata['saved_projects'] =  {
            'fname' : 'fname',
            'lname': 'lname'
        }
        userdata['user_id'] = userdata['_id']['$oid']
        userdata.pop('_id', None)

        data = {
            'data': {
                'user_id': userdata['user_id'],
                'update_dict': userdata                
            }            
        }

        url = '/update_user'

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        assert b'"status_code": 200' in res.data


    def test_signin_failed(self, client):
        data = {
            'data': {
                'username': 'admin2',
                'pwd': 'admin2'
            }
        }

        url = '/signin'

        res = client.post(url, data=json.dumps(data),
                          headers=self.userTest.headers)

        assert b'404 Not Found' in res.data
    
    
