from app import app, db
from app.models.admin_models import School
from mongoengine.queryset.visitor import Q

def get_all_schools(offset, size):
    return School.objects.only(
        '_id',
        'name',
        'address',
        'teachers',
        'administrator_id'
    ).skip(offset).limit(size)

def search_school(search):
    return School.objects(Q(name__icontains=search) | Q(address__icontains=search) | Q(administrator_id__icontains=search))


def upsert_school(school_dict):
    school = School(**school_dict)
    school.save()
    return (True, school)

def update_school(school_id, update_dict):
    School.objects.get_or_404(id=school_id).update(**update_dict)
    return (True, "")

def get_school(admin_id):
    res = School.objects(administrator_id=admin_id)
    school = res[0]
    school.id = str(school.id)
    return (True, school.id)

def get_school_using_id(school_id):
    return School.objects.get_or_404(id=school_id)


def delete_school(school_id):
    school = School.objects.get_or_404(id=school_id)
    school.delete()
    return (True, "")


def get_students_from_users(usertype):
    return User.objects(Q(user_type__icontains=usertype)).only('_id', 'first_name', 'last_name', 'username', 'user_type', 'email')


def add_student_to_school(student_id, school_id):
    """
    Add a student to a school
    Args:
        student_id   : ObjectId
        school_id    : ObjectId
    """
    school = get_school_using_id(school_id)
    school.student_list.append(student_id)
    school.save()
    return (True, "")


def delete_student_from_school(student_id, school_id):
    """
    Deletes a student from a school
    Args:
        student_id    : ObjectId
        school_id     : ObjectId
    """
    school = get_school_using_id(school_id)
    school.student_list.remove(student_id)
    school.save()
    return (True, "")

