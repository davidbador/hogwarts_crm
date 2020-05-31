import json
import datetime


class Course:

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def created_at():
        return datetime.datetime.now().isoformat()

    @staticmethod
    def updated_at():
        return datetime.datetime.now().isoformat()

    def __init__(self, course_name, professor_first_name, professor_last_name,
                 location, creation_time, last_update_time):
        self.course_name = str(course_name)
        self.professor_first_name = str(professor_first_name)
        self.professor_last_name = str(professor_last_name)
        self.location = str(location)
        self.creation_time = str(creation_time)
        self.last_update_time = str(last_update_time)
