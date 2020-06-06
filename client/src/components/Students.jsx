import React from 'react';
import { students } from '../lib/UserFunctions';
import '../App.css';

class Students extends React.Component {
    constructor() {
        super();
        this.state = {
            students: []
        }
    }

    componentDidMount() {
        this.loadStudents()
    }

    loadStudents = async () => {
        const response = await students()
        this.setState({
            students: [response.data]
        })
    }

    render() {
        return (
            <div className="container">
                <h1 className="text-center">Students</h1>
                <table className="table col-md-6 mx-auto">
                    <tbody>
                        <tr>
                            <td>ID</td>
                            <td>First Name</td>
                            <td>Last Name</td>
                            <td>Email</td>
                        </tr>
                        {this.state.students.map((el) =>
                            el.students.map((c, i) => (
                                <tr key={i}>
                                    <td>{c._id}</td>
                                    <td>{c.first_name}</td>
                                    <td>{c.last_name}</td>
                                    <td>{c.email}</td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        )
    }
}

export default Students