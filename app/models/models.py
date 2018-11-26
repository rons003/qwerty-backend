from app import app, db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class User(db.DynamicDocument):
    """
    Users of the Code Gakko Application.
    Users are either students or admin
    """
    first_name = db.StringField(max_length = 50, required = True)
    last_name = db.StringField(max_length = 50, required = True)
    username = db.StringField(max_length = 128, required = True, unique=True)
    pwd = db.StringField(max_length=128, required=True)
    email = db.StringField()
    # date_joined = db.DateTimeField(required=True)
    date_joined = db.FloatField()
    groups = db.ListField(db.StringField())
    # 0 - student, 1 - teacher, 2 - admin
    user_type = db.IntField(required=True)
    saved_projects = db.DictField()
    type_fields = db.DictField()
    assignment_progress = db.StringField()
    chapter_item_progress = db.StringField()
    chapter_progress = db.StringField()
    photo_icon = db.StringField()
    school_ids = db.ListField(db.StringField())
    meta = {"strict": False}

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.objects.get_or_404(id=data['id'])
        return user


class Group(db.DynamicDocument):
    """
    A group can represent a collection of students and teachers.
    This is where the learning happens.
    The curriculum field contains multiple Chapters.
    """
    name = db.StringField(required=True)
    admins = db.ListField(db.StringField())
    students = db.ListField(db.StringField())
    chapters = db.ListField(db.StringField())

    #Unused
    date_created = db.FloatField()
    visible_chapters = db.ListField()
    assignments = db.ListField()
    meta = {"strict": False}

class Chapter(db.DynamicDocument):
    """
    Part of a whole curriculum in a group
    Contains multiple Challenges.
    """
    name = db.StringField(required=True)
    desc = db.StringField()
    chapter_items = db.ListField()
    difficulty = db.IntField()
    topics = db.ListField()
    meta = {"strict": False}

class ChapterItem(db.DynamicDocument):
    """
    A chapter contains multiple ChapterItems.
    They can be of 3 item_types: "slides", "video", and "challenge"
    "slides" and "video" items have urls, "challenge" items do not
    """
    name = db.StringField(required=True)
    item_type = db.StringField(required=True)
    url = db.StringField()
    challenge_id = db.StringField()

class Challenge(db.DynamicDocument):
    """
    A challenge is part of a Chapter and
    poses a particular problem for users to solve.
    """
    name = db.StringField(required=True, unique=True)
    desc = db.StringField()
    hint = db.StringField()
    instructions = db.StringField()
    gif_url = db.StringField()
    solutions = db.ListField(db.StringField())
    sprites = db.ListField()
    toolbox = db.DictField()
    initial_blocks = db.ListField()
    correct_patterns = db.DictField()

    meta = {"strict": False}

class Assignment(db.DynamicDocument):
    """
    Assignment
    """
    challenge_id = db.StringField()
    due_date = db.FloatField()
    # due_date = db.DateTimeField()

class Sprite(db.DynamicDocument):
    """
    A Sprite object
    """
    name = db.StringField()
    x = db.FloatField()
    y = db.FloatField()
    width = db.FloatField()
    height = db.FloatField()
    enabled = db.BooleanField()

class ChallengeSave(db.DynamicDocument):
    """
    A Challenge Save object
    """
    user_id = db.StringField()
    challenge_id = db.StringField()
    # List of Sprites
    phaser_state = db.StringField()
    blockly_state = db.StringField()

class Project(db.DynamicDocument):
    """
    A Project Save Object
    """
    user_id = db.StringField()
    user_name = db.StringField()
    name = db.StringField()
    date_created = db.FloatField()
    phaser_state = db.StringField()
    blockly_state = db.StringField()

class Batchmate(db.DynamicDocument):
    """
    A group can represent a collection of students and teachers.
    This is where the learning happens.
    The curriculum field contains multiple Chapters.
    """
    name = db.StringField(required=True)
    teachers = db.ListField(db.StringField())
    students = db.ListField(db.StringField())
    chapters = db.ListField(db.StringField())

    #Unused
    date_created = db.FloatField()
    visible_chapters = db.ListField()
    assignments = db.ListField()
    meta = {"strict": False}
