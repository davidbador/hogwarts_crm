import pymongo
from flask import Flask, request, json
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from model.user import Student
from model.course import Course
from datetime import datetime

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'hogwarts'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/hogwarts'
app.config['JWT_SECRET_KEY'] = 'secret'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)


class DataLayer:

    def get_students(self):
        students = self.__db.students.find()
        return students

    def get_student_by_id(self, student_id):
        student_dict = self.__db.students.find_one({"_id": ObjectId(student_id)})
        if student_dict:
            resp = 'true'
        else:
            resp = 'false'
        return resp

    def get_students_by_date(self, year, month, day):
        date = datetime(year, month, day)
        string_date = date.strftime('%Y-%m-%d')
        students = self.__db.students.count({"creation_time": string_date})
        return str(students)

    def get_pie_existing(self):
        new_data = {"riddikulus": 0, "obliviate": 0, "lumos": 0, "nox": 0, "protego": 0, "expelliarmus": 0, "accio": 0,
                    "wingardium leviosa": 0, "expecto patronum": 0, "alohomora": 0}
        students = self.get_students()
        for i in students:
            for j in i['existing_magic_skills']:
                for key in new_data:
                    if j == key:
                        new_data[key] += 1
        return new_data

    def get_pie_desired(self):
        new_data = {"riddikulus": 0, "obliviate": 0, "lumos": 0, "nox": 0, "protego": 0, "expelliarmus": 0, "accio": 0,
                    "wingardium leviosa": 0, "expecto patronum": 0, "alohomora": 0}
        students = self.get_students()
        for i in students:
            for j in i['desired_magic_skills']:
                for key in new_data:
                    if j == key:
                        new_data[key] += 1
        return new_data

    def get_student_existing_by_id(self, student_id):
        student_dict = self.__db.students.find_one({"_id": ObjectId(student_id)})
        if student_dict:
            resp = student_dict.get('existing_magic_skills')
        else:
            resp = {'status': 'Can not find this user id in the system'}
        return resp

    def get_student_desired_by_id(self, student_id):
        student_dict = self.__db.students.find_one({"_id": ObjectId(student_id)})
        if student_dict:
            resp = student_dict.get('desired_magic_skills')
        else:
            resp = {'status': 'Can not find this user id in the system'}
        return resp

    def get_student_courses_by_id(self, student_id):
        student_dict = self.__db.students.find_one({"_id": ObjectId(student_id)})
        if student_dict:
            resp = dumps(student_dict.get('interested_courses'))
        else:
            resp = {'status': 'Can not find this user id in the system'}
        return resp

    @staticmethod
    def create_student_from_dict(student_dict):
        try:
            student = Student(student_dict['first_name'], student_dict['last_name'], student_dict['email'],
                              student_dict['password'], student_dict['admin'], student_dict['creation_time'],
                              student_dict['last_update_time'], student_dict['existing_magic_skills'],
                              student_dict['desired_magic_skills'], student_dict['interested_courses'])
            return student
        except Exception as e:
            print(e)

    def create_student(self):
        time = Student.created_at()
        first_name = request.get_json()['first_name']
        last_name = request.get_json()['last_name']
        email = request.get_json()['email']
        password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
        if self.__db.students.find_one({"email": email}):
            added_student = {'status': 'The email is already in the system!'}
        else:
            new_student = Student(first_name, last_name, email, password, False, time, time, {}, {}, [])
            self.__db.students.insert_one(new_student.__dict__)
            added_student = {'status': 'The student has been added!'}
        return added_student

    def add_course_to_student(self, student_id, course_name):
        try:
            update_time = Student.updated_at()
            if self.__db.students.find_one({"_id": ObjectId(student_id), "interested_courses": {'$in': [course_name]}}):
                add_course = {"status": 'The course already exists in this section!'}
            else:
                self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                                       {"$set": {"last_update_time": update_time}})

                self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                                       {"$push": {"interested_courses": course_name}})

                add_course = {"status": 'student is now interested in this course!'}
            return add_course
        except Exception as e:
            print(e)

    def delete_course_from_student(self, student_id, course_name):
        try:
            update_time = Student.updated_at()
            if self.__db.students.find_one({"_id": ObjectId(student_id), "interested_courses": {'$in': [course_name]}}):

                self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                                       {"$set": {"last_update_time": update_time}})

                self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                                       {"$pull": {"interested_courses": course_name}})

                delete_course = {'status': 'The course is now deleted!'}
            else:
                delete_course = {'status': 'The course is not in this section!'}
            return delete_course
        except Exception as e:
            print(e)

    def add_update_existing_skill(self, student_id, skill_name, score):
        try:
            update_time = Student.updated_at()
            spells = self.__db.skills.find()
            add_update_spell = ''
            for i in spells:
                for j in i['spells']:
                    if j == skill_name:
                        self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                                               {"$set": {"last_update_time": update_time,
                                                                         "existing_magic_skills." + skill_name: score}})
                        add_update_spell = {'status': 'The skill is now added!'}
                    elif j != skill_name:
                        if skill_name not in i['spells']:
                            add_update_spell = {'status': 'The skills is not in the predefined list!'}
                        else:
                            continue
                    return add_update_spell
        except Exception as e:
            print(e)

    def add_update_desired_skill(self, student_id, skill_name, score):
        try:
            update_time = Student.updated_at()
            spells = self.__db.skills.find()
            add_update_spell = ''
            for i in spells:
                for j in i['spells']:
                    if j == skill_name:
                        self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                                               {"$set": {"last_update_time": update_time,
                                                                         "desired_magic_skills." + skill_name: score}})
                        add_update_spell = {'status': 'The skill is now added!'}
                    elif j != skill_name:
                        if skill_name not in i['spells']:
                            add_update_spell = {'status': 'The skill is not in the predefined list!'}
                        else:
                            continue
                    return add_update_spell
        except Exception as e:
            print(e)

    def delete_desired_skill(self, student_id, skill_name):
        try:
            update_time = Student.updated_at()
            if self.__db.students.find_one(
                    {"_id": ObjectId(student_id), "desired_magic_skills": {skill_name: {"$exists": True}}}):

                self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                                       {"$set": {"last_update_time": update_time}})

                self.__db.students.find_one_and_update({"_id": ObjectId(student_id)},
                                                       {"$unset": {"desired_magic_skills."+skill_name: 1}})

                delete_desired = {'status': 'The skill has been removed'}
            else:
                delete_desired = {'status': 'The skill is not within the set'}
            return delete_desired
        except Exception as e:
            print(e)

    def delete_student(self, student_id, secret_code):
        try:
            if self.__db.students.find_one({"_id": ObjectId(student_id)}) and secret_code == 'always':
                self.__db.students.delete_one({"_id": ObjectId(student_id)})
                students = {"status": 'The student has been deleted!'}
            else:
                students = {"status": 'The student id is not in the system!'}
            return students
        except Exception as e:
            print(e)

    def get_courses(self):
        courses = dumps(self.__db.courses.find())
        return courses

    def get_course_by_id(self, course_id):
        try:
            course_dict = self.__db.courses.find_one({"_id": ObjectId(course_id)})
            if course_dict:
                course = self.create_course_from_dict(course_dict)
                resp = app.response_class(response=json.dumps(course.to_json()),
                                          status=200,
                                          mimetype="application/json")
            else:
                resp = {'status': 'The course is not in the system'}
            return resp
        except Exception as e:
            print(e)

    @staticmethod
    def create_course_from_dict(course_dict):
        try:
            course = Course(course_dict['course_name'], course_dict['professor_first_name'],
                            course_dict['professor_last_name'], course_dict['location'],
                            course_dict["creation_time"], course_dict["last_update_time"])
            return course
        except Exception as e:
            print(e)

    def get_skills(self):
        skills = self.__db.skills.find()
        all_skills = ''
        for doc in skills:
            all_skills = dumps(doc['spells'])
        return all_skills

    def __init__(self):
        self.__client = pymongo.MongoClient('localhost', 27017)
        self.__db = self.__client['hogwarts']
