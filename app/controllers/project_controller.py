from app import app, db
from app.models.models import User, Group, Chapter, Challenge, Project, ChallengeSave, Sprite
from app.models.templates import *
import datetime
import math
import itertools

def get_all_projects_of_user(user_id):
    """
    Fetches all projects belonging to a user
    """
    projects = Project.objects(user_id=user_id)
    return projects

def get_all_projects_of_group(student_ids):
    """
    Fetches all projects belonging to a group
    """
    projects = [get_all_projects_of_user(student_id) for student_id in student_ids]
    return list(itertools.chain.from_iterable(projects))

def convert_sprites_objects_to_dict(sprites_json):
    sprites = []
    for sprite in sprites_json:
        s = Sprite(**sprite)
        s.save()
        sprites.append(s.id)
    return sprites

def convert_project_object_to_dict(project_dict):
    """
    The json POST data should be according to JavaScript specifications.
    This functions converts that to a Python dictionary with proper construction
    of ChallengeSave and Sprite objects so that we can create/update a Project
    object
    """
    sprites_json = project_dict["phaser_state"]
    sprites = convert_sprites_objects_to_dict(sprites_json)
    project_dict["phaser_state"] = sprites
    return project_dict

def create_project(project_dict):
    project_dict["date_created"] = unix_time_millis(datetime.datetime.now())
    # project_dict = convert_project_object_to_dict(project_dict)
    project = Project(**project_dict)
    project.save()
    return (True, project)

def delete_project(project_id):
    """
    Deletes project from database.
    Args:
        project_id         : ObjectId
            Finds project by ObjectId
    Returns:
        (Bool, Result)
    """
    project = Project.objects.get_or_404(id=project_id)
    project.delete()
    return (True, "success")

def update_project(project_id, update_dict):
    """
    Updates a given project based on the keys and values
    supplied in the update_dict. The keys must match the
    list of attributes that the project has
    """
    # update_dict = convert_project_object_to_dict(update_dict)
    # try:
    Project.objects.get_or_404(id=project_id).update(**update_dict)
    return (True, "success")
    # except Exception, e:
    #     return (False, repr(e))

def get_project(project_id):
    """
    Gets project from database
    Args:
        project_id         : ObjectId
            Finds project by ObjectId
    Returns:
        Project object
    """
    project = Project.objects.get_or_404(id=project_id)
    return project

"""
Getters
"""
def get_simple_attribute(project_id, key):
    """
    Returns the attribute of the object, where the attribute is usually
    single-valued.
    """
    attrs = project_template.keys()
    assert key in attrs
    # try:
    project = get_project(project_id)
    return project[key]

def unix_time_millis(dt):
    return math.ceil((dt - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000.0)
