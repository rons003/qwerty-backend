from app import app
from app.tests.class_test import UserTest
import os, json
import pytest


@pytest.mark.skip(reason="no way of currently testing this")

class TestDashboard(object):

    userTest = UserTest()

    @pytest.fixture
    def client(self):    
        client = app.test_client()        
        yield client

    def test_signin(self, client):    

        data = {
            'data': {
                'username': 'admin',
                'pwd': 'admin'
            }
        }

        url = '/signin'

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)

        if jsonres['user']:
            if jsonres['user']['_id']:
                  if jsonres['user']['_id']['$oid']:
                        self.userTest.id = jsonres['user']['_id']['$oid']                   

    def test_get_all_projects_of_user(self, client):
        
        data = {
            'data': {
                'user_id': self.userTest.id
            }
        }

        url = '/get_all_projects_of_user'

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)
    
        assert len(jsonres['projects']) == 1

    def test_get_user_groups(self, client):

        data = {
            'data': {
                'user_id': self.userTest.id
            }
        }

        url = '/get_user_groups'    

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)
    
        
        for g in jsonres['groups']:        
            self.userTest.group_id = g
            break

        assert  len(jsonres['groups']) == 3

    def test_getgroup(self, client):
        data = {
            'data': {
                'group_id': self.userTest.group_id
            }
        }

        url = '/get_group'

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)    
        jres2 = json.loads(jsonres['group'])
        
        assert len(jres2['_id']['$oid']) == 24

    def test_get_user_objects_list(self, client):
        data = {
            'data': {
                'group_id': self.userTest.group_id,
                'user_type' : 1
            }
        }

        url = '/get_user_objects_list'

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)
        assert len(jsonres['data']) == 2

    def test_get_chapter_objects_list(self, client):
        data = {
            'data': {
                'group_id': self.userTest.group_id
            }
        }

        url = '/get_chapter_objects_list'

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)
        self.userTest.chapter_id = jsonres['data'][0]['_id']['$oid']
        assert len(jsonres['data']) == 5
        
    def test_get_assignment_objects_list(self, client):
        data = {
            'data': {
                'group_id': self.userTest.group_id
            }
        }

        url = '/get_assignment_objects_list'

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)
        assert jsonres['status_code'] == 200

    def test_get_chapter(self, client):
        
        data = {
            'data': {
                'chapter_id': self.userTest.chapter_id
            }
        }

        url = '/get_chapter'

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)
        
        jsonres = json.loads(res.data)
        jres2 = json.loads(jsonres['chapter'])
        assert jres2['name'] == 'Chapter 1: Introducing GakkoBlocks'

    def test_get_chapter_item_objects_list(self, client):

        data = {
            'data': {
                'chapter_id': self.userTest.chapter_id
            }
        }

        url = '/get_chapter_item_objects_list'

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)

        for ci in jsonres['chapter_items']:
            if 'challenge_id' in  ci:
                self.userTest.challenge_id = ci['challenge_id']
                break
    
        assert len(self.userTest.challenge_id) == 24

    def test_get_challenge(self, client):
        
        data = {
            'data': {
                'challenge_id': self.userTest.challenge_id
            }
        }

        url = '/get_challenge'

        res = client.post(url, data=json.dumps(
            data), headers=self.userTest.headers)

        jsonres = json.loads(res.data)

        print jsonres


    
    
