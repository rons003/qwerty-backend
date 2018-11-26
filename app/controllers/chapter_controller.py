from app import app, db
from app.models.models import User, Group, Chapter, Challenge, ChapterItem
from app.models.templates import *
import app.controllers.challenge_controller as challenge_c
import app.controllers.chapter_item_controller as chapter_item_c
import datetime

"""
Functions
"""


def add_chapter_item_to_chapter(chapter_item_id, chapter_id):
    chapter = get_chapter_using_id(chapter_id)
    chapter.chapter_items.append(chapter_item_id)
    chapter.save()
    return (True, "")


def delete_chapter_item_from_chapter(chapter_item_id, chapter_id):
    chapter = get_chapter_using_id(chapter_id)
    chapter.chapter_items.remove(chapter_item_id)
    chapter.save()
    return (True, "")


def add_challenge(challenge_id, chapter_id):
    """
    Add a challenge to a chapter
    Args:
        challenge_id      : ObjectId
        chapter_id        : ObjectId
    """
    chapter = get_chapter(chapter_id)
    chapter.challenges.append(challenge_id)
    chapter.completed_challenges[challenge_id] = False
    chapter.save()
    return (True, "")


def delete_challenge(challenge_id, chapter_id):
    """
    Deletes a challenge from a chapter
    Args:
        challenge_id      : ObjectId
        chapter_id        : ObjectId
    """
    chapter = get_chapter(chapter_id)
    chapter.challenges.remove(challenge_id)
    chapter.completed_challenges.pop(challenge_id)
    chapter.save()
    return (True, "")


def get_challenge(challenge_id, chapter_id):
    """
    Finds a challenge in a chapter and returns it
    """
    chapter = get_chapter(chapter_id)
    return (challenge_id in chapter.challenges,
            Challenge.objects.get_or_404(id=challenge_id))


def get_chapter_challenges(chapter_id):
    """
    Gets all challenges belonging to chapter
    """
    challenge_ids = get_simple_attribute(chapter_id, "challenges")
    challenges = challenge_c.get_challenge_objects_list(challenge_ids)
    return challenges


def get_chapters():
    chapters = Chapter.objects
    return chapters


def get_chapters_in_json():
    """
    Finds all chapters
    """
    chapters = [chapter.to_json() for chapter in Chapter.objects]
    return chapters


def complete_challenge(challenge_id, chapter_id):
    """
    Marks a challenge as complete
    """
    chapter = get_chapter(chapter_id)
    chapter.completed_challenges[challenge_id] = True
    chapter.save()
    return (True, "")


def uncomplete_challenge(challenge_id, chapter_id):
    """
    Marks a challenge as incomplete
    """
    chapter = get_chapter(chapter_id)
    chapter.completed_challenges[challenge_id] = False
    chapter.save()
    return (True, "")


"""
CRUD Functions
"""


def get_all_chapter(offset, size):
    return Chapter.objects.skip(offset).limit(size)


def create_chapter(chapter_dict):
    chapter = Chapter(**chapter_dict)
    chapter.save()
    return (True, chapter)


def delete_chapter(chapter_id):
    chapter = Chapter.objects.get_or_404(id=chapter_id)
    chapter.delete()
    return (True, "")


def get_chapter(chapter_id):
    chapter = Chapter.objects.get_or_404(id=chapter_id)
    return chapter


def get_chapter_using_school(module_id):
    return Chapter.objects(module_id=module_id)


def get_chapter_using_id(chapter_id):
    return Chapter.objects.get_or_404(id=chapter_id)


def update_chapter(chapter_id, update_dict):
    Chapter.objects.get_or_404(id=chapter_id).update(**update_dict)
    return (True, "")


"""
Getters
"""


def get_simple_attribute(chapter_id, key):
    """
    Returns the attribute of the object, where the attribute is usually
    single-valued. For Chapters, this includes difficulty, slides_url, etc.
    """
    attrs = chapter_template.keys()
    assert key in attrs
    chapter = get_chapter(chapter_id)
    return chapter[key]


def get_chapter_objects_list(chapter_ids):
    chapters = [get_chapter(chapter_id) for chapter_id in chapter_ids]
    return chapters
