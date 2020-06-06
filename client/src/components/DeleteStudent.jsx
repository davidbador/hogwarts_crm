import React from 'react';
import { removeStudent, studentById } from '../lib/UserFunctions';

class DeleteStudent extends React.Component {
    constructor() {
        super();
        this.state = {
            value: ''
        }
        this.onChange = this.onChange.bind(this)
    }

    onChange = (event) => {
        this.setState({
            value: event.target.value
        })
    }

    deleteStudent = (id) => {
        studentById(id).then(response => {
            if (response.data === true && this.state.value.length === 24) {
                let secretCode = prompt('please enter the secret code')
                if (secretCode === 'always') {
                    removeStudent(id, secretCode)
                } else {
                    alert('wrong secret code!')
                }
            } else {
                alert('student does not exist!')
            }
        })
    }

    render() {
        return (
            <div className="delete">
                <input type="text" value={this.state.value} onChange={(event) => this.onChange(event)} />
                <button type="button" className="btn btn-danger" onClick={() => this.deleteStudent(this.state.value)}>Remove Student</button>
            </div>
        )
    }
}

export default DeleteStudent