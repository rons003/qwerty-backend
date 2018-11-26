from app import app, db
from app.models.models import User
import datetime

class School(db.DynamicDocument):
    """
    School or a Learning
    Center or an Organization
    """
    name = db.StringField(required=True)
    address = db.StringField()
    teachers = db.ListField(db.StringField())
    administrator_id = db.StringField()
    student_list = db.ListField(db.StringField())
    meta = {"strict": False}


class Section(db.DynamicDocument):
    """
    School Section     
    """
    name = db.StringField(required=True)
    student_list = db.ListField(db.StringField())
    section_start = db.StringField()
    section_end = db.StringField()

    meta = {"strict": False}

class Module(db.DynamicDocument):
    """
    Modules
    """
    name = db.StringField(required=True)
    desc = db.StringField()
    teacher = db.StringField()
    section_list = db.ListField(db.StringField())
    chapter_list = db.ListField(db.StringField())

    meta = {"strict": False}
    

class Teacher(db.DynamicDocument):
    """
    Teachers Associated to one or more School
    """    
    sections = db.ListField(db.StringField())
    modules = db.ListField(db.StringField())
    meta = {"strict": False}


class Student(db.DynamicDocument):
    """
    Student of a Particular School
    """
    user_id = db.StringField()
    school_id = db.StringField(required=True)
    teacher_id = db.StringField(required=True)
    sections = db.ListField(db.StringField())
    modules = db.ListField(db.StringField())
    meta = {"strict": False}
