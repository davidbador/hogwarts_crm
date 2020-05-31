from flask import Flask, json
from db.dataLayer import DataLayer

app = Flask(__name__)

dataLayer = DataLayer()


@app.route("/students")
def get_students():
    students = dataLayer.get_students()
    resp = app.response_class(response=json.dumps(students),
                              status=200,
                              mimetype='application/json')
    return resp


@app.route("/students/<string:student_id>")
def get_student_by_id(student_id):
    student = dataLayer.get_student_by_id(student_id)
    resp = app.response_class(response=json.dumps(student.to_json()),
                              status=200,
                              mimetype="application/json")
    return resp


@app.route("/students/register", methods=["POST"])
def add_student():
    dataLayer.create_student()
    resp = {'status': 'new student added!'}
    return resp


@app.route("/students/login", methods=['POST'])
def log_in_student():
    dataLayer.log_in_student()


@app.route("/professors/login", methods=['POST'])
def log_in_student():
    dataLayer.log_in_professor()


@app.route("/students/<string:student_id>/update_first_name/<string:first_name>", methods=["POST"])
def update_student_first_name(student_id, first_name):
    dataLayer.update_first_name(student_id, first_name)
    resp = {"status": 'student\'s first name has been updated!'}
    return resp


@app.route("/students/<string:student_id>/update_last_name/<string:last_name>", methods=["POST"])
def update_student_last_name(student_id, last_name):
    dataLayer.update_last_name(student_id, last_name)
    resp = {"status": 'student\'s last name has been updated!'}
    return resp


@app.route("/students/<string:student_id>/add_course/<string:course_id>", methods=['POST'])
def add_course_to_student(student_id, course_id):
    dataLayer.add_course_to_student(student_id, course_id)
    resp = {"status": 'student is now interested in this course!'}
    return resp


@app.route("/students/<string:student_id/remove_course/<string:course_id>", methods=['DELETE'])
def delete_course_from_student(student_id, course_id):
    dataLayer.delete_course_from_student(student_id, course_id)
    resp = {"status": 'the course has been removed!'}
    return resp


@app.route("/students/<string:student_id>/add_skill/existing/<string:skill_name>/<string:score>",
           methods=['POST'])
def add_existing_skill(student_id, skill_name, score):
    dataLayer.add_existing_skill(student_id, skill_name, score)
    resp = {"status": 'skill added to student\'s existing skills'}
    return resp


@app.route("/students/<string:student_id>/update_skill/existing/<string:skill_name>/<string:score>", methods=['POST'])
def update_existing_skill(student_id, skill_name, score):
    dataLayer.update_existing_skill(student_id, skill_name, score)
    resp = {"status": 'the skill\'s score has been updated!'}
    return resp


@app.route("/students/<string:student_id>/add_skill/desired/<string:skill_name>/<string:score>", methods=['POST'])
def add_desired_skill(student_id, skill_name, score):
    dataLayer.add_desired_skill(student_id, skill_name, score)
    resp = {"status": 'skill added to student\'s desired skills'}
    return resp


@app.route("/students/<string:student_id>/update_skill/desired/<string:skill_name>/<string:score>", methods=['POST'])
def update_desired_skill(student_id, skill_name, score):
    dataLayer.update_desired_skill(student_id, skill_name, score)
    resp = {"status": 'the skill\'s score has been updated!'}
    return resp


@app.route("/students/<string:student_id>/remove_skill/desired/<string:skill_name>", methods=['DELETE'])
def remove_desired_skill(student_id, skill_name):
    dataLayer.delete_desired_skill(student_id, skill_name)
    resp = {"status": 'the skill has been removed!'}
    return resp


@app.route("/students/delete/<string:student_id>", methods=["DELETE"])
def delete_student_by_id(student_id):
    students = dataLayer.delete_student(student_id)
    resp = app.response_class(response=json.dumps(students),
                              status=200,
                              mimetype="application/json")
    return resp


@app.route("/courses")
def get_courses():
    courses = dataLayer.get_courses()
    resp = app.response_class(response=json.dumps(courses),
                              status=200,
                              mimetype='application/json')
    return resp


@app.route("/courses/<string:course_id>")
def get_course_by_id(course_id):
    course = dataLayer.get_course_by_id(course_id)
    resp = app.response_class(response=json.dumps(course.to_json()),
                              status=200,
                              mimetype="application/json")
    return resp


@app.route("/courses/<string:course_name>/<string:professor_first_name>_<string:professor_last_name>/<string:location>",
           methods=["POST"])
def add_course(course_name, professor_first_name, professor_last_name, location):
    dataLayer.create_course(course_name, professor_first_name, professor_last_name, location)
    resp = {'status': 'new course added!'}
    return resp


@app.route("/student/<string:course_id>/update_course_name/<string:course_name>", methods=["POST"])
def update_course_name(course_id, course_name):
    dataLayer.update_course_name(course_id, course_name)
    resp = {"status": 'course\'s name has been updated!'}
    return resp


@app.route("/courses/<string:course_id>/update_professor_first_name/<string:professor_first_name>",
           methods=["POST"])
def update_professor_first_name(course_id, professor_first_name):
    dataLayer.update_professor_first_name(course_id, professor_first_name)
    resp = {"status": 'professor\'s first name has been updated!'}
    return resp


@app.route("/courses/<string:course_id>/update_professor_last_name/<string:professor_last_name>",
           methods=["POST"])
def update_professor_last_name(course_id, professor_last_name):
    dataLayer.update_professor_last_name(course_id, professor_last_name)
    resp = {"status": 'professor\'s last name has been updated!'}
    return resp


@app.route("/courses/<string:course_id>/update_location/<string:location>", methods=["POST"])
def update_location(course_id, location):
    dataLayer.update_location(course_id, location)
    resp = {"status": 'course location has been updated!'}
    return resp


@app.route("/courses/delete/<string:course_id>", methods=["DELETE"])
def delete_course_by_id(course_id):
    courses = dataLayer.delete_course(course_id)
    resp = app.response_class(response=json.dumps(courses),
                              status=200,
                              mimetype="application/json")
    return resp


if __name__ == "__main__":
    app.run()
