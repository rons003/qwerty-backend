from app import app, db
from app.models.models import User, Group, Chapter, Challenge, Assignment
from app.models.templates import *
import datetime

"""
Functions
"""
def set_due_date(assignment_id, due_date):
    """
    Set the due date of an assignment
    :param: due_date    : DateTime Object
    """
    a = get_assignment(assignment_id)
    a.due_date = due_date
    a.save()
    return (True, "")

"""
CRUD Functions
"""
def create_assignment(assignment_dict):
    # challenge = Challenge(**assignment_dict["challenge"])
    # challenge.save()
    # assignment_dict["challenge"] = challenge
    a = Assignment(**assignment_dict)
    a.save()
    return (True, a)

def delete_assignment(assignment_id):
    a = Assignment.objects.get_or_404(id=assignment_id)
    a.delete()
    return (True, "")

def get_assignment(assignment_id):
    a = Assignment.objects.get_or_404(id=assignment_id)
    return a

# def update_assignment(assignment_id, update_dict):
#     Assignment.objects.get_or_404(id=assignment_id).update(**update_dict)
#     return (True, "")

"""
Getters
"""
def get_simple_attribute(assignment_id, key):
    attrs = assignment_template.keys()
    assert key in attrs
    a = get_assignment(assignment_id)
    return a[key]

def get_assignment_objects_list(assignment_ids):
    assignments = [get_assignment(assignment_id) for assignment_id in assignment_ids]
    return assignments
