from app import app, db
from app.models.admin_models import Section
from app.models.models import User
#from mongoengine.queryset.visitor import Q

"""
Functions
"""


def add_student_to_section(student_id, section_id):
    """
    Add a student to a section
    Args:
        student_id    : ObjectId
        section_id    : ObjectId
    """
    section = get_section_using_id(section_id)
    for stud_id in student_id:
        section.student_list.append(stud_id)
    section.save()
    return (True, "")


def delete_student_from_section(student_id, section_id):
    """
    Deletes a student from a section
    Args:
        student_id    : ObjectId
        section_id       : ObjectId
    """
    section = get_section_using_id(section_id)
    for stud_id in student_id:
        section.student_list.remove(stud_id)
    section.save()
    return (True, "")


"""
CRUD
"""


def get_all_sections(offset, size):
    return Section.objects.only(
        '_id',
        'school_id',
        'name',
        'student_list',
    ).skip(offset).limit(size)


def search_section(search):
    return Section.objects(name__icontains=search)


def create_section(section_dict):
    section = Section(**section_dict)
    section.save()
    return (True, section)


def update_section(section_id, update_dict):
    Section.objects.get_or_404(id=section_id).update(**update_dict)
    return (True, "")


def get_section_using_id(section_id):
    return Section.objects.get_or_404(id=section_id)


def get_section(school_id):
    return Section.objects(school_id=school_id).only(
        '_id',
        'school_id',
        'name',
        'student_list',
    )


def delete_section(section_id):
    section = Section.objects.get_or_404(id=section_id)
    section.delete()
    return (True, "")


def get_student_from_school(school_id):
    return User.objects(school_id=school_id, user_type=0)
