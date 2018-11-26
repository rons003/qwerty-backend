"""
Module that imports data into the database
1) Upload challenges from "app/data/data.json"
2) Upload chapters from "app/data/chapters.json"
3) Parse new users from "app/data/classes.csv"
   Created usernames and passwords at "app/data/outclasses.csv"
   Firstname and lastname combination must be unique
4) Delete all challenges
5) Delete all chapters
6) Delete all users
7) Delete all groups
8) Delete all data
"""
import app.controllers.group_controller as gc
import app.controllers.user_controller as uc
import app.controllers.challenge_controller as cc
import app.controllers.chapter_controller as chc
import app.controllers.chapter_item_controller as cic
from app.models import templates as tp
from app.models.models import *
import csv
import json
import operator
import os

IN_FILE_DATA = "app/data/data.json"
IN_FILE_CHAPTERS = "app/data/chapters.json"
IN_FILE_CLASS = "app/data/classes.csv"
OUT_FILE_CLASS = "app/data/classesInDatabase.csv"
OUT_FILE_PWDS = "app/data/passwords.txt"

def clear_challenges():
    ans = ""
    while ans != "yes":
        ans = raw_input("Do you really wish to delete challenges? yes/no: ")
        if ans == "no":
            return

    for c in [Challenge]:
        c.objects.delete()

def clear_chapters():
    ans = ""
    while ans != "yes":
        ans = raw_input("Do you really wish to delete chapters? yes/no: ")
        if ans == "no":
            return

    for c in [Chapter]:
        c.objects.delete()

def clear_users():
    ans = ""
    while ans != "yes":
        ans = raw_input("Do you really wish to delete users? yes/no: ")
        if ans == "no":
            return

    for c in [User]:
        c.objects.delete()
    try:
        os.remove(OUT_FILE_PWDS)
    except OSError:
        pass
    
def clear_groups():
    ans = ""
    while ans != "yes":
        ans = raw_input("Do you really wish to delete all existing groups from the database? yes/no: ")
        if ans == "no":
            return

    for c in [Group]:
        c.objects.delete()
    try:
        os.remove(OUT_FILE_CLASS)
    except OSError:
        pass

def upload_challenges():
    clear_challenges()
    print "Uploading challenges from data.json to database"
    with open(IN_FILE_DATA) as data_file:    
        challenge_objects = json.load(data_file)

    for challenge_object in challenge_objects:
        cc.create_challenge(challenge_object)
    print "Done"

def upload_chapters():
    clear_chapters()
    print "Uploading all chapters from chapters.json to database"
    with open(IN_FILE_CHAPTERS) as data_file:    
        chapter_objects = json.load(data_file)

    for chapter_object in chapter_objects:
        for index, chapter_item in enumerate(chapter_object["chapter_items"]):
            if chapter_item["item_type"] == "challenge":
                chapter_item["challenge_id"] = str(cc.get_challenge_id_by_name(chapter_item["name"]))
            chapter_object["chapter_items"][index] = str(cic.create_chapter_item(chapter_item)[1].id)
        chc.create_chapter(chapter_object)

    for group in gc.get_all_groups():
        group["chapters"] = map(lambda x: str(x.id), chc.get_chapters())
        group.save()
    # TODO: Right now, all groups have access to all classes, in the future, different groups might be allocated different chapters.

    print "Done"

def upload_groups_and_users():
    class_file_exists = os.path.isfile(OUT_FILE_CLASS) 

    with open(IN_FILE_CLASS, "rb") as in_file, \
         open(OUT_FILE_CLASS, "ab") as out_file_class, \
         open(OUT_FILE_PWDS, "a") as out_file_pwds:

        reader = csv.reader(in_file)
        writer = csv.writer(out_file_class)
        
        # Skip the fist header line
        header_row = reader.next()

        if not class_file_exists:
            writer.writerow(header_row)
        
        # Sort the data by class
        reader = sort_data_by_class(reader)

        # TODO: Regular expressions on fields to check if fields are properly formatted
        for row in reader:
            assert row[0] #Class Name
            assert row[1] #First Name
            assert row[2] #Last Name
            assert row[5] #Is Admin

        #TODO: Worry about teachers providing shitty formatting
        
        # Remove starting and trailing spaces
        row[0] = row[0].strip()
        row[1] = row[1].strip()
        row[2] = row[2].strip()
        row[3] = row[3].strip()
        row[4] = row[4].strip()
        row[5] = row[5].strip()

        for row in reader:
            group_name = row[0]
            if gc.group_already_in_database(group_name):
                group = gc.get_group_by_group_name(group_name)
            else:
                group = create_group_and_associate_super_admin(group_name)                

            if uc.user_already_in_database(row[1], row[2]):
                user = uc.get_user_by_first_and_last_name(row[1], row[2])
                row[3] = user["username"]
                row[6] = "ERR: USER ALR EXISTS"
            else: 
                user_type = 1 if row[5] == 'y' or row[5] == 'Y' else 0
                user_template = tp.admin_template if user_type is 1 else tp.student_template
                user_template["first_name"] = row[1]
                user_template["last_name"] = row[2]

                if (row[3] == ""):
                    row[3] = uc.generate_unique_user_name(row[1], row[2])
                else:
                    row[3] = row[3].replace(" ", "")
                    row[3] = row[3].lower()
                    if uc.username_already_in_database(row[3]):
                        print "Username already taken, generating unique username..."
                        row[3] = uc.generate_unique_user_name(row[1], row[2])
                        print "    Username " + row[3] + " generated!"

                user_template["username"] = row[3]
                user_template["email"] = row[4]
                user_template["user_type"] = user_type
                
                row[6] = uc.generate_password()

                # Store the hashed password into database
                user_template["pwd"] = uc.hash_password(row[6])
                
                # Write into passwords.txt file
                out_file_pwds.write(user_template["username"] + "\n")
                out_file_pwds.write(row[6] + "\n")

                user = uc.create_user(user_template)[1]
                print "    User " + user["username"] + " created!"
                
                # Write file into outfile
                writer.writerow(row)

            associate_user_and_group(user, group)            

##################################################
#         SUPERUSER HELPER FUNCTIONS             #
##################################################

def super_admin_in_database():
    return uc.user_already_in_database("super", "admin")

def add_super_admin_user():
    if super_admin_in_database():
        print "super admin already in database"
        return

    user_type = 1
    user_template = tp.admin_template
    user_template["first_name"] = "super"
    user_template["last_name"] = "admin"
    user_template["username"] = "admin"
    user_template["email"] = "superadmin@superadmin.com"
    user_template["user_type"] = 1
    user_template["pwd"] = uc.hash_password("admin")
    return uc.create_user(user_template)[1]

def create_group_and_associate_super_admin(group_name):
    # Get super admins
    if super_admin_in_database():
        super_user = uc.get_user_by_first_and_last_name("super", "admin")
    else:
        super_user = add_super_admin_user()

    # Create group
    grp_template = tp.group_template
    grp_template["name"] = group_name
    group = gc.create_group(grp_template)[1]
    print "    Group " + group["name"] + " created"
    
    # Associate super admin
    associate_user_and_group(super_user, group)
    return group

##################################################
#            HELPER FUNCTIONS                    #
##################################################

def associate_user_and_group(user, group):
    if gc.add_user(user.id, group.id, user["user_type"])[0]:
        if uc.add_group(user.id, group.id)[0]:
            print "    " + user["username"] + " added to " + group["name"] + "!"

def sort_data_by_class(csv_reader):
    return sorted(csv_reader, key = operator.itemgetter(0))

##################################################
#            MAIN LOOP                           #
##################################################

if __name__ == "__main__":
    repeat = True
    while repeat:
        ans = raw_input("""
    1) Upload challenges from app/data/data.json and chapters from app/data/chapters.json
    2) Parse and upload new users from app/data/classes.csv
    3) Delete users and groups only
    4) Delete all data
    5) Exit

Your choice: """)
    
        repeat = False
        if ans == "1":
            upload_challenges()
            upload_chapters()
        elif ans == "2":
            upload_groups_and_users()
        elif ans == "3":
            clear_users()
            clear_groups()
        elif ans == "4":
            clear_challenges()
            clear_chapters()
            clear_users()
            clear_groups()
        elif ans == "5":
            break
        else:
            repeat = True
