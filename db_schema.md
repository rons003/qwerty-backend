# Database schema



## User

* first_name (string)
* last_name (string)
* username (string)
* pwd (string)
* email (string)
* date_joined (datetime)
* groups (list)
* user_type (int)
  * 0 - student
  * 1 - admin
* saved_projects (dictionary)
  * Key: Challenge id (string)
  * Value: ChallengeSave object
* assignment_progress (dictionary)
  * Key: Challenge id (string)
  * Value: completion (boolean)
* chapter_progress (dictionary)
  - Key: Chapter id (string)
  - Value: completion (boolean)
* chapter_item_progress (dictionary)
  - Key: ChapterItem id (string)
  - Value: completion (boolean)



## Group

* name (string)
* students (list)
* admins (list)
* current_chapter (string)
  * id of chapter
* date_created (datetime)
* group_icon (URL)
  * url of icon
* chapters (list)
* assignments (dictionary)
  - Key: Challenge id (string)
  - Value: Due date (datetime)
* chapter_progress (dict)
  * Key: Chapter id (string)
  * Value: completion (boolean)
* challenge_progress (dict)
  * Key: Challenge id (string)
  * Value: completion (boolean)



## Chapter

* difficulty (int)

  * 0 - Newbie
  * 1 - Beginner
  * 2 - Intermediate
  * 3 - Advanced

* chapter_icon (URL)

  * url of icon

* desc (string)

* topic (string)

  * Variables, For loops, etc

* slides (URL)

* challenges (list)

  ​

## Challenge

* difficulty (int)
  * 0 - Newbie
  * 1 - Beginner
  * 2 - Intermediate
  * 3 - Advanced
* desc (string)
* topic (string)
* gif_url (URL)
