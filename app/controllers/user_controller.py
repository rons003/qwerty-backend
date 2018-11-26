from app import app, db
from app.models.models import User, Group, Chapter, Challenge
from app.models.templates import *
# import app.controllers.badge_controller as bc
import app.controllers.group_controller as gc
import app.controllers.challenge_controller as cc
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine.queryset.visitor import Q
import datetime
import math
import string
import random


def login(username, pwd):
    res = User.objects(username=username)
    if len(res) == 0:
        return False
    else:
        user = res[0]
        user.id = str(user.id)
        if check_password_hash(user.pwd, pwd):
            token = user.generate_auth_token()
            return token
        else:
            return None


def add_group(user_id, group_id):
    """
    Adds a group to user's groups list
    Also creates a key in the 'students' dictionary
    """
    user = get_user(user_id)
    if any(groups_of_user == str(group_id) for groups_of_user in user["groups"]):
        print "Group already exists on user!"
        return (False, "fail")

    user.groups.append(str(group_id))
    user.save()
    return (True, "success")


def add_user_to_group(adder_id, to_be_added_id, group_id):
    """
    Adds a user to a group's list
    """
    group = gc.get_group(group_id)
    adder = get_user(adder_id)
    to_be_added = get_user(to_be_added_id)
    adder.students[str(group.id)].append(to_be_added_id)
    to_be_added.groups.append(str(group.id))
    to_be_added.assignments[str(group.id)] = []

    adder.save()
    to_be_added.save()
    return (True, "success")


def delete_user_from_group(deleter_id, to_be_deleted_id, group_id):
    """
    Deletes user from a group's list
    """
    group = gc.get_group(group_id)
    deleter = get_user(deleter_id)
    to_be_deleted = get_user(to_be_deleted_id)
    deleter.students[str(group.id)].remove(to_be_deleted_id)
    to_be_deleted.groups.remove(str(group.id))
    deleter.save()
    to_be_deleted.save()
    return (True, "success")


def get_users_from_school(school_name):
    """
    Get all students belonging to a particular school
    """
    usernames = [str(user.username)
                 for user in User.objects(school_name=school_name)]
    return usernames


def get_all_usernames(usertype):
    """
    Gets usernames of a specified type.
    Args:
        usertype    : int
        0 - students
        1 - parents
        2 - teachers
        3 - all usernames
    """
    if usertype == 3:
        usernames = [str(user.username) for user in User.objects]
    else:
        usernames = [str(user.username)
                     for user in User.objects(admin_level=usertype)]
    return usernames

def get_student_from_school(id):
    return User.objects(Q(id=id[0]) & Q(id=id[1]))


def get_all_users(offset, size):
    return User.objects.only('_id', 'first_name', 'last_name', 'username', 'user_type', 'email').skip(offset).limit(size)

def get_all_students(offset, size):
    return User.objects(user_type=0).only('_id', 'first_name', 'last_name', 'username', 'user_type', 'email').skip(offset).limit(size)


def get_user_groups(user_id):
    """
    Gets all group_ids that the user belongs to
    Args:
        user_id     : ObjectId
    """
    return get_simple_attribute(user_id, "groups")


def assign_challenge(user_id, group_id, challenge_id, points, due_date):
    user = get_user(user_id)
    challenge = {
        "challenge_id": challenge_id, "points": points,
        "due_date": due_date
    }
    user.assignments[str(group_id)].append(challenge)
    user.save()
    return (True, "success")


def get_users_students(user_id):
    """
    For Admin/Teachers.
    Gets students from all groups that the admin manages.
    It will return a dictionary of the form:
        {
            group_id1: [user_id1, user_id2, ...]
            group_id2: ...
        }
    """
    user = get_user(user_id)
    return user.students


def reset_password(user_id, new_password):
    """
    Resets the password of the given user with given password.
    """
    # try:
    user = get_user(user_id)

    pwd = generate_password_hash(new_password)
    user.update(pwd=pwd)
    return (True, "success")


def update_user_password(user_id, old_password, new_password):
    """
    Updates a given user's password.
    """
    # try:
    user = get_user(user_id)

    # Check if old password matches
    if check_password_hash(user.pwd, old_password):
        pwd = generate_password_hash(new_password)
        user.update(pwd=pwd)
        return (True, "success")
    else:
        return (False, "fail")


"""
CRUD Functions
"""


def create_user(user_dict):
    """
    Function that creates a User
    Args:
        user_dict       :   dict
            A dictionary with all the relevant variables
            Must include first_name, last_name, username, pwd,
    """
    user_dict["date_joined"] = unix_time_millis(datetime.datetime.now())
    #user_dict["last_login"] = datetime.datetime.now()
    #user_dict["last_active"] = datetime.datetime.now()

    user = User(**user_dict)
    user.save()
    return (True, user)


def delete_user(user_id):
    """
    Deletes user from database.
    Args:
        user_id         : ObjectId
            Finds user by ObjectId
    Returns:
        (Bool, Result)
    """
    user = User.objects.get_or_404(id=user_id)
    user.delete()
    return (True, "success")


def get_user(user_id):
    """
    Gets user from database
    Args:
        user_id         : ObjetId
            Finds user by ObjectId
    Returns:
        User object
    """
    user = User.objects.get_or_404(id=user_id)
    return user


def get_user_by_first_and_last_name(first_name, last_name):
    user = User.objects.get_or_404(first_name=first_name, last_name=last_name)
    return user


def get_user_by_username(username):
    """
    Gets user from database
    Args:
        username         : str
            Finds user by username
    Returns:
        User object
    """
    # try:
    user = User.objects.get_or_404(username=username)
    return user
    # except Exception, e:
    #     return repr(e)


def username_already_in_database(username):
    return len(User.objects(username=username).limit(1)) is not 0


def user_already_in_database(first_name, last_name):
    return len(User.objects(first_name=first_name, last_name=last_name).limit(1)) is not 0


def update_user(user_id, update_dict):
    """
    Updates a given user based on the keys and values
    supplied in the update_dict. The keys must match the
    list of attributes that the user has
    """
    # try:
    User.objects.get_or_404(id=user_id).update(**update_dict)
    return (True, "success")
    # except Exception, e:
    #     return (False, repr(e))


"""
User Name and Pass Word generators and hashers
"""


def generate_unique_user_name(first_name, last_name):
    # Remove spaces
    first_name = first_name.replace(" ", "")
    last_name = last_name.replace(" ", "")

    # To lower case
    first_name = first_name.lower()
    last_name = last_name.lower()
    base = first_name + last_name
    username = first_name + last_name
    append_num = 1

    while username_already_in_database(username):
        username = base + str(append_num)
        append_num += 1

    return username


def generate_password():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))


def hash_password(plaintext_pwd):
    return generate_password_hash(plaintext_pwd)


"""
Getters
"""


def get_simple_attribute(user_id, key):
    """
    Returns the attribute of the object, where the attribute is usually
    single-valued. For Users, this includes current_level, date_created,
    group_url, etc.
    """
    attrs = student_template.keys()
    assert key in attrs
    # try:
    user = get_user(user_id)
    return user[key]
    # except Exception, e:
    #     return repr(e)


def get_user_objects_list(user_ids):
    users = [get_user(user_id) for user_id in user_ids]
    return users


def unix_time_millis(dt):
    return math.ceil((dt - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000.0)


# seach
def search_user(search, usertype):
    if usertype != 'all' and search != 'novalues':
        return User.objects(Q(user_type__icontains=usertype) & (Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(username__icontains=search))).only('_id', 'first_name', 'last_name', 'username', 'user_type', 'email')
    elif search == 'novalues' and usertype != 'all':
        return User.objects(user_type__icontains=usertype).only('_id', 'first_name', 'last_name', 'username', 'user_type', 'email')
    else:
        return User.objects(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(username__icontains=search)).only('_id', 'first_name', 'last_name', 'username', 'user_type', 'email')


def search_usertype(searchtype):
    return User.objects(Q(user_type__icontains=searchtype)).only('_id', 'first_name', 'last_name', 'username', 'user_type', 'email')


def get_teacher_using_school(school_id):
    user = User.objects(school_id=school_id,user_type=1)
    return user
