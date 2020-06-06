import React from 'react';
import { register } from '../lib/UserFunctions';
import '../App.css';

class addNewStudent extends React.Component {
    constructor() {
        super();
        this.state = {
            firstName: '',
            lastName: '',
            email: '',
            password: ''
        }
        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }

    onChange(event) {
        this.setState({ [event.target.name]: event.target.value })
    }

    onSubmit(event) {
        event.preventDefault()

        const newUser = {
            firstName: this.state.firstName,
            lastName: this.state.lastName,
            email: this.state.email,
            password: this.state.password
        }

        if (newUser.firstName === '' || newUser.lastName === '' || newUser.email === '' || newUser.password === '') {
            document.getElementById('danger').classList.remove('hide')
            setTimeout(() => {document.getElementById('danger').classList.add('hide')}, 7000)
        } else {
            register(newUser)
            document.getElementById('success').classList.remove('hide')
            setTimeout(() => {document.getElementById('success').classList.add('hide')}, 7000)
        }
    }

    render() {
        return (
            <div>
                <div className="container">
                    <div className="row">
                        <div className="col-md-6 mt-5 mx-auto">
                            <form noValidate onSubmit={this.onSubmit}>
                                <div className="form-group">
                                    <label htmlFor="firstName">First Name</label>
                                    <input type="text" className="form-control" name="firstName" placeholder="Enter Your First Name" value={this.state.firstName} onChange={this.onChange} />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="lastName">Last Name</label>
                                    <input type="text" className="form-control" name="lastName" placeholder="Enter Your Last Name" value={this.state.lastName} onChange={this.onChange} />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="email">Email Address</label>
                                    <input type="email" className="form-control" name="email" placeholder="Enter Email" value={this.state.email} onChange={this.onChange} />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="password">Password</label>
                                    <input type="password" className="form-control" name="password" placeholder="Enter Password" value={this.state.password} onChange={this.onChange} />
                                </div>
                                <button type="submit" className="btn btn-lg btn-primary btn-block">
                                    Add New Student
                                </button>
                                <div id="success" className="alert alert-success hide" role="alert">
                                    New student added!
                                </div>
                                <div id="danger" className="alert alert-danger hide" role="alert">
                                    Please make sure all fields are filled in!
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default addNewStudent