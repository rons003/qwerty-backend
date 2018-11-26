# Specs List for Code Gakko App Backend

## Classes

* User
	* Attributes
		* user_id
		* name
		* username
		* age
		* bio
		* email
		* current_level
		* current_points
		* photo_icon
		* school_name
		* country
		* date_joined
		* fb_token
		* number_level_attempts
		* number_levels_completed
		* badges
		* last_login (last session start)
		* last_active (last activity on website)
		* gender
		* recovery_email
		* admin_level (student/guardian/teacher)
		* groups
		* children (for parents)
		* students (for teachers)
		* friends

* Group
	* Attributes
		* group_id
		* users
		* admins
		* user_emails
		* admin_emails
		* current_level
		* current_points
		* date_created
		* last_active
		* active_users
		* group_url
		* group_icon

* Challenge
	* Attributes
		* level_id
		* difficulty
		* points
		* badges
		* level_icon
		* desc
		* slides_url
		* level_type (block or syntax)

* Badge
	* Attributes
		* badge_id
		* title
		* desc
		* logo


## Features

* As a teacher, I want to receive organized reports on students' progress
* As a teacher, I want the platform to be easy to use when teaching concepts
* As a teacher, I want to see on a dashboard the progress of individual students and the class as a whole
* As a parent, I want to receive feedback / progress on my child's progress
* As a teacher, I want different subscription options


## Pricing scheme

* Annual / monthly / weekly subscription model (for school / parents / individuals)
* Pay per creation of group
* Teacher training course


## Stack (For Backend)

* Python (Flask)
* MongoDB - MongoEngine
* Digital Ocean
