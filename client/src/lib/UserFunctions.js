import axios from 'axios';

const baseURL = 'http://127.0.0.1:5000'

export const register = newUser => {
    return axios.post(`${baseURL}/students/register`, {
        first_name: newUser.firstName,
        last_name: newUser.lastName,
        email: newUser.email,
        password: newUser.password
    }).then(res => {
        console.log("Registered")
    })
}

export const login = user => {
    return axios.post(`${baseURL}/students/login`, {
        email: user.email,
        password: user.password
    }).then(res => {
        localStorage.setItem('usertoken', res.data.token)
        return res.data.token
    }).catch(err => {
        console.log(err)
    })
}

export const students = () => {
    return axios.get(`${baseURL}/students`)
}

export const studentById = (id) => {
    return axios.get(`${baseURL}/students/${id}`)
}

export const studentsDateCount = (year, month, day) => {
    return axios.get(`${baseURL}/students/${year}/${month}/${day}`)
}

export const studentsPieExisting = () => {
    return axios.get(`${baseURL}/students/pie/existing`)
}

export const studentsPieDesired = () => {
    return axios.get(`${baseURL}/students/pie/desired`)
}

export const singleStudentExisting = (id) => {
    return axios.get(`${baseURL}/students/${id}/existing`)
}

export const singleStudentDesired = (id) => {
    return axios.get(`${baseURL}/students/${id}/desired`)
}

export const singleStudentCourses = (id) => {
    return axios.get(`${baseURL}/students/${id}/courses`)
}

export const addCourseToStudent = (studentId, courseName) => {
    return axios.post(`${baseURL}/students/${studentId}/add_course/${courseName}`)
}

export const removeCourseFromStudent = (studentId, courseName) => {
    return axios.delete(`${baseURL}/students/${studentId}/remove_course/${courseName}`)
}

export const addUpdateExistingSkill = (studentId, skillName, score) => {
    return axios.post(`${baseURL}/students/${studentId}/add_update_skill/existing/${skillName}/${score}`)
}

export const addUpdateDesiredSkill = (studentId, skillName, score) => {
    return axios.post(`${baseURL}/students/${studentId}/add_update_skill/desired/${skillName}/${score}`)
}

export const removeStudent = (studentId, secretCode) => {
    return axios.delete(`${baseURL}/students/delete/${studentId}/${secretCode}`)
}

export const courses = () => {
    return axios.get(`${baseURL}/courses`)
}

export const singleCourse = (id) => {
    return axios.get(`${baseURL}/courses/${id}`)
}

export const skills = () => {
    return axios.get(`${baseURL}/skills`)
}