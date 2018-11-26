from app import app, db
from app.models.models import User, Group, Chapter, Challenge
from app.models.templates import *
import datetime

"""
CRUD Functions
"""
def create_challenge(challenge_dict):
    """
    Function that creates a Challenge
    Args:
        challenge_dict       :   dict
            A dictionary with all the relevant variables
    """
    challenge = Challenge(**challenge_dict)
    challenge.save()
    return (True, challenge)
    # return (True, challenge)
    # except Exception, e:
    #     return (False, repr(e))


def delete_challenge(challenge_id):
    """
    Deletes challenge from database.
    Args:
        challenge_id         : ObjectId
            Finds challenge by ObjectId
    """
    challenge = Challenge.objects.get_or_404(id=challenge_id)
    challenge.delete()
    return (True, "success")
    # except Exception, e:
    #     return (False, repr(e))

def get_challenge_id_by_name(challenge_name):
    """
    Gets challenge from database
    Args:
        challenge_name        : string
            Finds challenge by name
    Returns:
        Challenge id
    """
    # try:
    challenge = Challenge.objects.get_or_404(name=challenge_name)
    return challenge.id

def get_challenge(challenge_id):
    """
    Gets challenge from database
    Args:
        challenge_id         : ObjectId
            Finds challenge_id by ObjectId
    Returns:
        Challenge object
    """
    # try:
    challenge = Challenge.objects.get_or_404(id=challenge_id)
    return challenge
    # except Exception, e:
    #     return repr(e)

def get_challenges():
    """
    Gets all available challenges
    """
    challenges = [challenge for challenge in Challenge.objects]
    return challenges

def update_challenge(challenge_id, update_dict):
    """
    Updates a given challenge based on the keys and values
    supplied in the update_dict. The keys must match the
    list of attributes that the challenge has
    """
    # try:
    Challenge.objects.get_or_404(id=challenge_id).update(**update_dict)
    return (True, "success")
    # except Exception, e:
    #     return (False, repr(e))

"""
Getters
"""
def get_simple_attribute(challenge_id, key):
    """
    Returns the attribute of the object, where the attribute is usually
    single-valued. For Challenges, this includes difficulty, points, etc.
    """
    attrs = challenge_template.keys()
    assert key in attrs
    # try:
    challenge = get_challenge(challenge_id)
    return challenge[key]
    # except Exception, e:
    #     return repr(e)

def get_challenge_objects_list(challenge_ids):
    challenges = [get_challenge(challenge_id) for challenge_id in challenge_ids]
    return challenges
