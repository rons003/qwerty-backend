from app import app, db
from app.models.admin_models import Module


"""
Functions
"""


def add_section_to_module(section_id, module_id):
    """
    Add a section to a module
    Args:
        section_id    : ObjectId
        module_id        : ObjectId
    """
    module = get_module_using_id(module_id)
    module.section_list.append(section_id)
    module.save()
    return (True, "")


def add_chapter_to_module(chapter_id, module_id):
    """
    Add a section to a module
    Args:
        chapter_id    : ObjectId
        module_id        : ObjectId
    """
    module = get_module_using_id(module_id)
    module.chapter_list.append(chapter_id)
    module.save()
    return (True, "")


def delete_section_from_module(section_id, module_id):
    """
    Deletes a chap section from a module
    Args:
        section_id      : ObjectId
        module_id        : ObjectId
    """
    module = get_module_using_id(module_id)
    for sec_id in section_id:
        module.section_list.remove(sec_id)
    module.save()
    return (True, "")


def delete_chapter_from_module(chapter_id, module_id):
    """
    Delete a chap to a module
    Args:
        chapter_id    : ObjectId
        module_id        : ObjectId
    """
    module = get_module_using_id(module_id)
    for chap_id in chapter_id:
        module.chapter_list.remove(chap_id)
    module.save()
    return (True, "")


"""
CRUD
"""


def get_all_modules(offset, size):
    return Module.objects.only(
        '_id',
        'school_id',
        'name', 'desc',
        'teacher_list',
        'section_list',
        'chapter_list'
    ).skip(offset).limit(size)


def create_module(module_dict):
    module = Module(**module_dict)
    module.save()
    return (True, module)


def update_module(module_id, update_dict):
    Module.objects.get_or_404(id=module_id).update(**update_dict)
    return (True, "")


def get_module(school_id):
    return Module.objects(school_id=school_id)


def get_module_using_id(module_id):
    return Module.objects.get_or_404(id=module_id)


def delete_module(module_id):
    module = Module.objects.get_or_404(id=module_id)
    module.delete()
    return (True, "")
