from flask import Flask
from flask import jsonify
from flask import request
from flask import json
from db.dataLayer import DataLayer
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_cors import CORS


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'hogwarts'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/hogwarts'
app.config['JWT_SECRET_KEY'] = 'secret'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)

dataLayer = DataLayer()


@app.route("/students")
def get_students():
    students = dataLayer.get_students()
    all_students = []

    for i in students:
        all_students.append(i)

    response = app.response_class(response=(json.dumps({"students": all_students}, default=str)), status=200,
                                  mimetype="application/json")
    return response


@app.route("/students/<string:student_id>")
def get_student_by_id(student_id):
    return dataLayer.get_student_by_id(student_id)


@app.route("/students/<int:year>/<int:month>/<int:day>")
def get_students_by_date(year, month, day):
    return dataLayer.get_students_by_date(year, month, day)


@app.route("/students/pie/existing")
def get_pie_existing():
    return dataLayer.get_pie_existing()


@app.route("/students/pie/desired")
def get_pie_desired():
    return dataLayer.get_pie_desired()


@app.route("/students/<string:student_id>/existing")
def get_student_existing_by_id(student_id):
    return dataLayer.get_student_existing_by_id(student_id)


@app.route("/students/<string:student_id>/desired")
def get_student_desired_by_id(student_id):
    return dataLayer.get_student_desired_by_id(student_id)


@app.route("/students/<string:student_id>/courses")
def get_student_courses_by_id(student_id):
    return dataLayer.get_student_courses_by_id(student_id)


@app.route("/students/register", methods=["POST"])
def add_student():
    return dataLayer.create_student()


@app.route("/students/login", methods=['POST'])
def log_in_student():
    students = mongo.db.students
    email = request.get_json()['email']
    password = request.get_json()['password']

    response = students.find_one({'email': email})

    if response:
        if bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity={
                'id': str(response['_id']),
                'first_name': response['first_name'],
                'last_name': response['last_name'],
                'email': response['email'],
            })
            result = jsonify({'token': access_token})
        else:
            result = jsonify({"error": "Invalid username and password"})
    else:
        result = jsonify({"result": "No results found"})
    return result


@app.route("/students/<string:student_id>/add_course/<string:course_name>", methods=['POST'])
def add_course_to_student(student_id, course_name):
    return dataLayer.add_course_to_student(student_id, course_name)


@app.route("/students/<string:student_id>/remove_course/<string:course_name>", methods=['DELETE'])
def delete_course_from_student(student_id, course_name):
    return dataLayer.delete_course_from_student(student_id, course_name)


@app.route("/students/<string:student_id>/add_update_skill/existing/<string:skill_name>/<string:score>",
           methods=['POST'])
def add_update_existing_skill(student_id, skill_name, score):
    return dataLayer.add_update_existing_skill(student_id, skill_name, score)


@app.route("/students/<string:student_id>/add_update_skill/desired/<string:skill_name>/<string:score>",
           methods=['POST'])
def add_update_desired_skill(student_id, skill_name, score):
    return dataLayer.add_update_desired_skill(student_id, skill_name, score)


@app.route("/students/delete/<string:student_id>/<string:secret_code>", methods=["DELETE"])
def delete_student_by_id(student_id, secret_code):
    return dataLayer.delete_student(student_id, secret_code)


@app.route("/courses")
def get_courses():
    return dataLayer.get_courses()


@app.route("/courses/<string:course_id>")
def get_course_by_id(course_id):
    return dataLayer.get_course_by_id(course_id)


@app.route("/skills")
def get_skills():
    return dataLayer.get_skills()


if __name__ == "__main__":
    app.run()
