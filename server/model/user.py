import json
import datetime


class Student:

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def created_at():
        return datetime.datetime.now().date()

    @staticmethod
    def updated_at():
        return datetime.datetime.now().isoformat()

    def __init__(self, first_name, last_name, email, password, admin, creation_time, last_update_time,
                 existing_magic_skills, desired_magic_skills, interested_courses):
        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.email = str(email)
        self.password = str(password)
        self.admin = admin
        self.creation_time = str(creation_time)
        self.last_update_time = str(last_update_time)
        self.existing_magic_skills = existing_magic_skills
        self.desired_magic_skills = desired_magic_skills
        self.interested_courses = interested_courses
