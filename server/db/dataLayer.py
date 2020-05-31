import pymongo
from flask import Flask, request, jsonify
from bson import ObjectId
from bson.json_util import dumps
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from flask_cors import CORS

from model.user import Student
from model.course import Course

app = Flask(__name__)

bcrypt = Bcrypt(app)

CORS(app)


class DataLayer:

    def get_students(self):
        students = self.__db.students.find()
        student_list = []
        for doc in students:
            student_list.append(dumps(doc))
        return student_list

    def get_student_by_id(self, student_id):
        student_dict = self.__db.students.find_one({"_id": ObjectId(student_id)})
        student = self.create_student_from_dict(student_dict)
        return student

    @staticmethod
    def create_student_from_dict(student_dict):
        student = Student(student_dict['first_name'], student_dict['last_name'], student_dict['email'],
                          student_dict['password'], student_dict['creation_time'],
                          student_dict['last_update_time'], student_dict['existing_magic_skills'],
                          student_dict['desired_magic_skills'], student_dict['interested_courses'])
        return student

    def create_student(self):
        time = Student.created_at()
        first_name = request.get_json()['first_name']
        last_name = request.get_json()['last_name']
        email = request.get_json()['email']
        password = bcrypt.generate_password_hash(request.get_json()['password'].decode('utf-8'))
        new_student = Student(first_name, last_name, email, password, time, time, {}, {}, [])
        added_student = self.__db.students.insert_one(new_student.__dict__)
        return added_student

    def log_in_student(self):
        email = request.get_json()['email']
        password = request.get_json()['password']

        response = self.__db.students.find_one({'email': email})

        if response:
            if bcrypt.check_password_hash(response['password'], password):
                access_token = create_access_token(identity={
                    'first_name': response['first_name'],
                    'last_name': response['last_name'],
                    'email': response['email']
                })
                result = jsonify({'token': access_token})
            else:
                result = jsonify({"error": "invalid email and password"})
        else:
            result = jsonify({"result": "no results found"})
        return result

    def log_in_professor(self):
        email = request.get_json()['email']
        password = request.get_json()['password']

        response = self.__db.professors.find_one({'email': email})

        if response:
            if bcrypt.check_password_hash(response['password'], password):
                access_token = create_access_token(identity={
                    'first_name': response['first_name'],
                    'last_name': response['last_name'],
                    'email': response['email']
                })
                result = jsonify({'token': access_token})
            else:
                result = jsonify({"error": "invalid email and password"})
        else:
            result = jsonify({"result": "no results found"})
        return result

    def update_first_name(self, student_id, first_name):
        update_time = Student.updated_at()
        self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                               {"$set": {"first_name": first_name,
                                                         "last_update_time": update_time}})

    def update_last_name(self, student_id, last_name):
        update_time = Student.updated_at()
        self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                               {"$set": {"first_name": last_name,
                                                         "last_update_time": update_time}})

    def add_course_to_student(self, student_id, course_id):
        update_time = Student.updated_at()
        self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                               {"$set": {"last_update_time": update_time}},
                                               {"$push": {"interested_courses": course_id}})

    def delete_course_from_student(self, student_id, course_id):
        update_time = Student.updated_at()
        self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                               {"$set": {"last_update_time": update_time}},
                                               {"pull": {"interested_courses": course_id}})

    def add_existing_skill(self, student_id, skill_name, score):
        update_time = Student.updated_at()
        spells = self.__db.skills.find({}, {'spells': 1})
        for i in spells:
            for j in i['spells']:
                if j == skill_name:
                    self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                                           {"$set": {"last_update_time": update_time,
                                                                     "existing_magic_skills."+skill_name: score}})

    def update_existing_skill(self, student_id, skill_name, score):
        update_time = Student.updated_at()
        self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                               {"$set": {"last_update_time": update_time,
                                                         "existing_magic_skills."+skill_name: score}})

    def add_desired_skill(self, student_id, skill_name, score):
        update_time = Student.updated_at()
        spells = self.__db.skills.find({}, {'spells': 1})
        for i in spells:
            for j in i['spells']:
                if j == skill_name:
                    self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                                           {"$set": {"last_update_time": update_time,
                                                                     "desired_magic_skills."+skill_name: score}})

    def update_desired_skill(self, student_id, skill_name, score):
        update_time = Student.updated_at()
        self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                               {"$set": {"last_update_time": update_time,
                                                         "desired_magic_skills."+skill_name: score}})

    def delete_desired_skill(self, student_id, skill_name):
        update_time = Student.updated_at()
        self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                               {"$set": {"last_update_time": update_time}},
                                               {"$unset": {"desired_magic_skills."+skill_name: 1}})

    def delete_student(self, student_id):
        self.__db.students.delete_one({"_id": ObjectId(student_id)})
        students = self.get_students()
        return students

    def get_courses(self):
        courses = self.__db.courses.find()
        courses_list = []
        for doc in courses:
            courses_list.append(dumps(doc))
        return courses

    def get_course_by_id(self, course_id):
        course_dict = self.__db.courses.find_one({"_id": ObjectId(course_id)})
        course = self.create_course_from_dict(course_dict)
        return course

    @staticmethod
    def create_course_from_dict(course_dict):
        course = Course(course_dict['course_name'], course_dict['professor_first_name'],
                        course_dict['professor_last_name'], course_dict['location'],
                        course_dict["creation_time"], course_dict["last_update_time"])
        return course

    def create_course(self, course_name, professor_first_name, professor_last_name, location):
        time = Course.created_at()
        new_course = Course(course_name, professor_first_name, professor_last_name, location, time, time)
        added_course = self.__db.courses.insert_one(new_course.__dict__)
        return added_course

    def update_course_name(self, course_id, course_name):
        update_time = Course.updated_at()
        self.__db.courses.find_one_and_update({"_id": ObjectId(course_id)},
                                              {"$set": {"course_name": course_name,
                                                        "last_update_time": update_time}})

    def update_professor_first_name(self, course_id, professor_first_name):
        update_time = Course.updated_at()
        self.__db.courses.find_one_and_update({"_id": ObjectId(course_id)},
                                              {"$set": {"professor_first_name": professor_first_name,
                                                        "last_update_time": update_time}})

    def update_professor_last_name(self, course_id, professor_last_name):
        update_time = Course.updated_at()
        self.__db.courses.find_one_and_update({"_id": ObjectId(course_id)},
                                              {"$set": {"professor_last_name": professor_last_name,
                                                        "last_update_time": update_time}})

    def update_location(self, course_id, location):
        update_time = Course.updated_at()
        self.__db.courses.find_one_and_update({"_id": ObjectId(course_id)},
                                              {"$set": {"location": location,
                                                        "last_update_time": update_time}})

    def delete_course(self, course_id):
        self.__db.courses.delete_one({"_id": ObjectId(course_id)})
        courses = self.get_courses()
        return courses

    def __init__(self):
        self.__client = pymongo.MongoClient('localhost', 27017)
        self.__db = self.__client['hogwarts']
