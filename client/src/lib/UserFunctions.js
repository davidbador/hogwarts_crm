import axios from 'axios';

export const register = newUser => {
    return axios
    .post("students/register", {
        first_name: newUser.first_name,
        last_name: newUser.last_name,
        email: newUser.email,
        password: newUser.password
    })
    .then(res => {
        console.log("Registered")
    })
}

export const login = user => {
    return axios
    .post("students/login", {
        email: user.email,
        password: user.password
    })
    .then(res => {
        localStorage.setItem('userToken', res.data.token)
        return res.data.token
    })
    .catch(err => {
        console.log(err)
    })
}