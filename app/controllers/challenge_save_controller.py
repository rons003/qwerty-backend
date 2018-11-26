from app import app, db
from app.models.models import ChallengeSave, Sprite
from app.models.templates import *
import datetime

def get_challenge_save_for_user_and_challenge(user_id, challenge_id):
    challenge_save = ChallengeSave.objects(user_id=user_id, challenge_id=challenge_id).first()
    return challenge_save

def set_challenge_save_for_user_and_challenge(user_id, challenge_id, update_dict):
    # Fields must be in snake case

    result = ChallengeSave.objects(user_id=user_id, challenge_id=challenge_id).first()
    if result is None:
        challenge_save = ChallengeSave(**update_dict)
        challenge_save.save()
    else:
        challenge_save = result
        challenge_save.update(**update_dict)
    return (True, challenge_save)
