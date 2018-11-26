from app import app

class UserTest(object):

    def __init__(self):
        self.id = ''
        self.mimetype = 'application/json'
        self.headers = {
            'Content-Type': self.mimetype,
            'Accept': self.mimetype
        }
        self.group_id = ''
        self.chapter_id = ''
        self.challenge_id = ''

    
