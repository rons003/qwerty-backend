from app import app, db
from app.models.models import User, Group, Chapter, Challenge, Assignment
import app.controllers.chapter_controller as chapter_c
import app.controllers.challenge_controller as challenge_c
import app.controllers.assignment_controller as assignment_c
from app.models.templates import *
import datetime
import math

"""
Functions
"""
def add_assignment_to_group(group_id, assignment_dict):
    group = get_group(group_id)
    (_, assignment) = assignment_c.create_assignment(assignment_dict)
    assignment_id = assignment.id
    group.assignments.append(assignment_id)
    group.save()
    return (True, "")

def remove_assignment_from_group(group_id, assignment_id):
    group = get_group(gruop_id)
    group.assignments.remove(assignment_id)
    group.save()
    return (True, "")

def add_chapter(chapter_id, group_id):
    """
    Add a chapter to a group
    Args:
        chapter_id      : ObjectId
        group_id        : ObjectId
    """
    group = get_group(group_id)
    group.chapters.append(chapter_id)
    group.save()
    return (True, "")

def delete_chapter(chapter_id, group_id):
    """
    Deletes a chapter from a group
    Args:
        chapter_id      : ObjectId
        group_id        : ObjectId
    """
    group = get_group(group_id)
    group.chapters.remove(chapter_id)
    group.save()
    return (True, "")

def get_chapter(chapter_id, group_id):
    """
    Finds a chapter in a group and returns it
    """
    group = get_group(group_id)
    return (chapter_id in group.chapters,
            Chapter.objects.get_or_404(id=chapter_id))    

def add_user(user_id, group_id, list_type):
    """
    Adds a user to a group
    Args:
        user_id         : ObjectId
        group_id        : ObjectId
        list_type       : int
            0 for user list, 1 for admin list
    """
    assert list_type == 0 or list_type == 1
    # try:
    group = get_group(group_id)
    if any(user_in_group == str(user_id) for user_in_group in group["admins"]):
        print "Admin already exists in group!"
        return (False, "failure")
    elif any(user_in_group == str(user_id) for user_in_group in group["students"]):
        print "Student already exists in group!"
        return (False, "failure")

    if list_type == 0:
        group.students.append(str(user_id))
        group.save()
    elif list_type == 1:
        group.admins.append(str(user_id))
        group.save()
    return (True, "success")
    # except Exception, e:
    #     return (False, repr(e))

def delete_user(user_id, group_id, list_type):
    """
    Deletes user from a group
    Args:
        user_id         : ObjectId
        group_id        : ObjectId
        list_type       : int
            0 for user list, 1 for admin list
    """
    assert list_type == 0 or list_type == 1
    # try:
    group = get_group(group_id)
    if list_type == 0:
        group.users.remove(user_id)
        group.save()
    elif list_type == 1:
        group.admins.remove(user_id)
        group.save()
    return (True, "success")
    # except Exception, e:
    #     return (False, repr(e))

def get_user(user_id, group_id, list_type):
    """
    Gets user from a group
    Args:
        user_id         : ObjectId
        group_id        : ObjectId
        list_type       : int
            0 for user list, 1 for admin list
    Returns:
        2-tuple of (<bool>, <User>)
        where <bool> indicates membership and <User> is the User object
    """
    assert list_type == 0 or list_type == 1
    # try:
    group = get_group(group_id)
    if list_type == 0:
        res = (user_id in group.users, User.objects.get_or_404(id=user_id))
    elif list_type == 1:
        res = (user_id in group.admins, User.objects.get_or_404(id=user_id))
    return res
    # except Exception, e:
    #     return (False, repr(e))

def activate_user(user_id, group_id):
    """
    Adds user to the active_users list
    Args:
        user_id         : ObjectId
        group_id        : ObjectId
    """
    # try:
    group = get_group(group_id)
    group.active_users.append(user_id)
    group.save()
    return (True, "success")
    # except Exception, e:
    #     return (False, repr(e))

def deactivate_user(user_id, group_id):
    """
    Deletes user to the active_users list
    Args:
        user_id         : ObjectId
        group_id        : ObjectId
    """
    # try:
    group = get_group(group_id)
    group.active_users.remove(user_id)
    group.save()
    return (True, "success")
    # except Exception, e:
    #     return (False, repr(e))

"""
CRUD Functions
"""
def create_group(group_dict):
    """
    Function that creates a Group
    Args:
        group_dict       :   dict
            A dictionary with all the relevant variables
    """
    # try:
    group_dict["chapters"] = map(lambda x: str(x.id), chapter_c.get_chapters())
    group_dict["date_created"] = unix_time_millis(datetime.datetime.now())

    group = Group(**group_dict)
    group.save()
    return (True, group)
    # except Exception, e:
    #     return (False, repr(e))    

def delete_group(group_id):
    """
    Deletes group from database.
    Args:
        group_id         : ObjectId
            Finds group by ObjectId
    """
    # try:
    group = get_group(group_id)
    group.delete()
    return (True, "success")
    # except Exception, e:
    #     return (False, repr(e))

def get_all_groups():
    """
    Gets all groups from database
    Returns:
        Array of Group objects
    """
    return Group.objects

def get_group(group_id):
    """
    Gets group from database
    Args:
        group_id         : ObjectId
            Finds groupd_id by ObjectId
    Returns:
        Group object
    """
    # try:
    group = Group.objects.get_or_404(id=group_id)
    return group
    # except Exception, e:
    #     return repr(e)

def get_group_by_group_name(group_name):
    """
    Gets group from database
    Args:
        groupname         : str
            Finds Group by groupname
    Returns:
        Group object
    """
    # try:
    group = Group.objects.get_or_404(name=group_name)
    return group
    # except Exception, e:
    #     return repr(e)

def group_already_in_database(group_name):
    return len(Group.objects(name=group_name).limit(1)) is not 0

def update_group(group_id, update_dict):
    """
    Updates a given group based on the keys and values
    supplied in the update_dict. The keys must match the
    list of attributes that the group has
    """
    # try:
    Group.objects.get_or_404(id=group_id).update(**update_dict)
    return (True, "success")
    # except Exception, e:
    #     return (False, repr(e))

"""
Getters
"""
def get_users(group_id):
    """
    Returns list of 2-tuples, which include
    (user_id, user_type)
    """
    # try:
    group = get_group(group_id)
    students = [(user_id, 0) for user_id in group.students]
    admins = [(user_id, 1) for user_id in group.admins]
    return students + admins
    # except Exception, e:
    #     return repr(e)

def get_students(group_id):
    """
    Returns list of user_id
    """
    # try:
    group = get_group(group_id)
    students = [user_id for user_id in group.students]
    return students 

def get_emails(group_id):
    """
    Returns list of 2-tuples, which include
    (email, user_type)
    """
    # try:
    group = get_group(group_id)
    user_emails = [(email, 0) for email in group.user_emails]
    admin_emails = [(email, 1) for email in group.admin_emails]
    return user_emails + admin_emails
    # except Exception, e:
    #     return repr(e)

def get_simple_attribute(group_id, key):
    """
    Returns the attribute of the object, where the attribute is usually
    single-valued. For Groups, this includes current_level, date_created,
    group_url, etc.
    """
    attrs = group_template.keys()
    assert key in attrs
    # try:
    group = get_group(group_id)
    return group[key]
    # except Exception, e:
    #     return repr(e)

def get_chapter_objects_list(group_id):
    """
    Returns list of Chapter objects in a group
    """
    group = get_group(group_id)
    chapters = chapter_c.get_chapter_objects_list(group.chapters)
    return chapters

# def get_challenge_objects_list(group_id):
#     """
#     Returns list of Challenge objects in a group
#     """
#     group = get_group(group_id)
#     challenge = challenge_c.get_challenge_objects_list(group.challenges)
#     return challenge

def get_assignment_objects_list(group_id):
    """
    Returns list of Assignment objects in a group
    """
    group = get_group(group_id)
    assignments = assignment_c.get_assignment_objects_list(group.assignments)
    return assignments

def unix_time_millis(dt):
    return math.ceil((dt - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000.0)
