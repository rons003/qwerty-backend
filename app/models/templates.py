from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import Challenge
import datetime

admin_photo_icon = "./assets/img/profile-teacher.png"
student_photo_icon = "./assets/img/student01.png"
group_icon_url = "./assets/img/school-logo-xinmin.png"
slides_url = "https://docs.google.com/presentation/d/17oc-M_RcvGE_W7h6G1xqS8DbR1xPFSJhR0KaFju1YR0/embed?start=false&loop=false&delayms=10000"

student_template = {
    "first_name": "",
    "last_name": "",
    "username": "",
    "pwd": "",
    "email": "",
    "date_joined": "",
    "groups": [],
    "user_type": 0,
    "saved_projects": {},
    "assignment_progress": "{}",
    "chapter_item_progress": "{}",
    "chapter_progress": "{}",
    "photo_icon": student_photo_icon
}

admin_template = {
    "first_name": "",
    "last_name": "",
    "username": "",
    "email": "",
    "pwd": "",
    "date_joined": "",
    "groups": [],
    "user_type": 0,
    "saved_projects": {},
    "assignment_progress": "{}",
    "chapter_item_progress": "{}",
    "chapter_progress": "{}",
    "photo_icon": admin_photo_icon
}

group_template = {
    "name": "",
    "admins": [],
    "students": [],
    "chapters": [],
    "date_created": 0,
    "visible_chapters": [],
    "assignments": []
}

chapter_template = {
    "name": "",
    "desc": "",
    "chapter_items": [],
    "difficulty": 0,
    "topics": []
}

chapter_item_template = {
    "name": "",
    "item_type": "",
    "url": "",
    "challenge_id": ""
}

challenge_template = {
    "name": "",
    "desc": "",
    "hint": "",
    "instructions": "",
    "gif_url": "",
    "sprites": [],
    "toolbox": {},
    "initial_blocks": [],
    "correct_patterns": {}
}

assignment_template = {
    "challenge_id": "",
    "due_date": datetime.datetime.now()
}

project_template = {
    "user_id": "",
    "user_name": "",
    "name": "",
    "date_created": datetime.datetime.now(),
    "phaser_state": "",
    "blockly_state": ""
}
