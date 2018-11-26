from app import app, db
from app.models.models import ChapterItem
from app.models.templates import *

"""
Functions
"""


def get_chapter_items():
    chapter_items = ChapterItem.objects
    return chapter_items


"""
CRUD Functions
"""


def get_all_chapter_item(offset, size):
    return ChapterItem.objects.skip(offset).limit(size)


def create_chapter_item(chapter_item_dict):
    chapter_item = ChapterItem(**chapter_item_dict)
    chapter_item.save()
    return (True, chapter_item)


def delete_chapter_item(chapter_item_ids):
    for chapter_item_id in chapter_item_ids:
        chapter_item = ChapterItem.objects.get_or_404(id=chapter_item_id)
        chapter_item.delete()
    return (True, "")


def get_chapter_item(chapter_item_id):
    chapter_item = ChapterItem.objects.get_or_404(id=chapter_item_id)
    print vars(chapter_item)
    return chapter_item


def update_chapter_item(chapter_item_id, updated_chapter_item_dict):
    ChapterItem.objects.get_or_404(id=chapter_item_id).update(
        **updated_chapter_item_dict)
    return (True, "")


"""
Getters
"""


def get_simple_attribute(chapter_item_id, key):
    """
    Returns the attribute of the object, where the attribute is usually
    single-valued. For Chapters, this includes difficulty, slides_url, etc.
    """
    attrs = chapter_item_template.keys()
    assert key in attrs
    chapter_item = get_chapter_item(chapter_item_id)
    return chapter_item[key]


def get_chapter_item_objects_list(chapter_item_ids):
    chapter_items = [get_chapter_item(chapter_item_id)
                     for chapter_item_id in chapter_item_ids]
    return chapter_items
